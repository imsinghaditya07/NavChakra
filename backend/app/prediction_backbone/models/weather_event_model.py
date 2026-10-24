"""
Weather Event Model — The Core Forecaster.

Provides the shared upstream backbone feeding all downstream parameter models and animation engines:
1. Global/Synoptic Track:
   - Detects and tracks large-scale systems: cloud clusters, storm formation, cyclone genesis & path.
   - Outputs: system type (cyclone|storm|none), position, intensity, projected track (6h/24h/72h), confidence.
2. Local/Gridded Track:
   - Predicts continuous fields at block resolution:
     - Nowcasting (0–6h) for rapid convective bursts
     - Medium-range (1–7d) for synoptic monsoon evolution
   - Outputs: probabilistic rainfall, temperature, heat index, soil moisture, flood runoff risk.
"""

import os
import math
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone, timedelta
import numpy as np

from backend.app.prediction_backbone.schema import EventSchema, TrackPoint, FieldsSchema


class WeatherEventModel:
    """
    Core two-track meteorological forecaster.
    Combines empirical atmospheric physics with trained machine-learning models
    (scikit-learn GradientBoostingRegressor & Classifier) serialized to models/rainfall/.
    """

    def __init__(self, version: str = "aryasaarthi-backbone-v2.1.0"):
        self.version = version
        self.ml_rainfall_loaded = False
        self.topography_map = {}

        # Attempt to load trained ML artifacts if available
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
        models_dir = os.path.join(base_dir, "models")
        data_proc_dir = os.path.join(base_dir, "data", "processed")

        topo_path = os.path.join(data_proc_dir, "west_bengal_district_topography.json")
        if os.path.exists(topo_path):
            try:
                with open(topo_path, "r", encoding="utf-8") as f:
                    self.topography_map = json.load(f)
            except Exception:
                pass

        rainfall_dir = os.path.join(models_dir, "rainfall")
        p50_path = os.path.join(rainfall_dir, "rainfall_p50_model.joblib")
        p10_path = os.path.join(rainfall_dir, "rainfall_p10_model.joblib")
        p90_path = os.path.join(rainfall_dir, "rainfall_p90_model.joblib")
        clf_path = os.path.join(rainfall_dir, "rainfall_prob_classifier.joblib")
        meta_path = os.path.join(rainfall_dir, "model_metadata.json")

        if all(os.path.exists(p) for p in [p50_path, p10_path, p90_path, clf_path, meta_path]):
            try:
                import joblib
                self.rf_p50 = joblib.load(p50_path)
                self.rf_p10 = joblib.load(p10_path)
                self.rf_p90 = joblib.load(p90_path)
                self.rf_clf = joblib.load(clf_path)
                with open(meta_path, "r", encoding="utf-8") as f:
                    self.rainfall_meta = json.load(f)
                self.ml_rainfall_loaded = True
            except Exception:
                self.ml_rainfall_loaded = False

    # =========================================================================
    # TRACK 1: GLOBAL / SYNOPTIC TRACK (Cyclone & Storm Genesis & Path)
    # =========================================================================
    def predict_synoptic_event(
        self,
        lat: float,
        lon: float,
        atmospheric_data: Dict[str, Any],
        forecast_time: Optional[datetime] = None
    ) -> EventSchema:
        """
        Detects active cyclone, depression, or severe storm system in the vicinity of (lat, lon)
        and projects 6h, 24h, and 72h steering trajectories.
        """
        now = forecast_time or datetime.now(timezone.utc)
        dist_maritime_km = atmospheric_data.get("dist_maritime_km", 600.0)
        sst_c = atmospheric_data.get("sst_c", 28.5)
        vws = atmospheric_data.get("vertical_wind_shear_ms", 12.0)
        cape = atmospheric_data.get("cape_j_kg", 2000.0)
        mslp = atmospheric_data.get("mslp_hpa", 1005.0)
        delta_tb = atmospheric_data.get("delta_tb_15m", -2.0)

        # 1. Evaluate Cyclogenesis Potential Index (CPI) over Bay of Bengal & Arabian Sea
        # Conditions: SST > 26.5 C, Low vertical wind shear (< 15 m/s), low central MSLP (< 1002 hPa)
        is_maritime_subdomain = dist_maritime_km < 950.0
        cpi = 0.0
        if is_maritime_subdomain and sst_c >= 26.5:
            # Normalized formula based on Kotal et al. (IMD Cyclogenesis Genesis Parameter)
            sst_term = max(0.0, (sst_c - 26.5) / 3.0)
            shear_term = max(0.1, (25.0 - vws) / 20.0)
            mslp_term = max(0.0, (1010.0 - mslp) / 15.0)
            cpi = sst_term * shear_term * mslp_term

        # Check proximity to known active monsoonal systems or severe squall lines
        # In Indian waters: Bay of Bengal cyclones typically recurve toward Odisha/West Bengal/Bangladesh
        is_cyclone = (cpi >= 0.55 and mslp <= 998.0) or (dist_maritime_km < 400.0 and sst_c > 29.0 and vws < 10.0)
        is_severe_storm = (cape >= 2600.0 and delta_tb <= -8.0) or (mslp < 1002.0 and not is_cyclone)

        if is_cyclone:
            event_type = "cyclone"
            intensity = float(np.clip(0.60 + cpi * 0.35, 0.60, 0.98))
            confidence = float(np.clip(0.85 + (sst_c - 28.0) * 0.04, 0.70, 0.94))
            name = "Deep Depression BOB-02" if intensity < 0.75 else "Severe Cyclonic Storm DANA"
            category = "Deep Depression" if intensity < 0.75 else "Severe Cyclonic Storm (Cat 1/2)"
            base_wind = 75.0 + intensity * 60.0
            base_press = 994.0 - intensity * 16.0

            # Compute steering track (Beta-advection towards North-Northwest across Bay of Bengal / East Coast)
            track = []
            for h in [6, 24, 72]:
                vt = now + timedelta(hours=h)
                # Recurvature physics: moves northwest initially, then bends northward
                d_lat = (h / 24.0) * 1.8 + (0.4 if h > 24 else 0.0)
                d_lon = -(h / 24.0) * 1.2 + (0.6 if h > 24 else -0.3)
                decay_factor = 1.0 if h <= 24 else 0.88  # slight decay after landfall
                track.append(TrackPoint(
                    horizon_hours=h,
                    valid_time=vt.isoformat(),
                    lat=round(lat + d_lat, 3),
                    lon=round(lon + d_lon, 3),
                    intensity=round(intensity * decay_factor, 2),
                    wind_speed_kmh=round(base_wind * decay_factor, 1),
                    pressure_hpa=round(base_press + (1.0 - decay_factor) * 12.0, 1)
                ))

        elif is_severe_storm:
            event_type = "storm"
            intensity = float(np.clip(0.35 + (cape / 4000.0) * 0.40, 0.30, 0.80))
            confidence = float(np.clip(0.78 + abs(delta_tb) * 0.015, 0.65, 0.90))
            name = "Mesoscale Convective Storm Cell"
            category = "Severe Thunderstorm / Squall System"
            base_wind = 52.0 + intensity * 35.0
            base_press = 1003.0 - intensity * 6.0

            # Meso storm track (typically propagates East-Southeast with mid-tropospheric steering)
            track = []
            for h in [6, 24, 72]:
                vt = now + timedelta(hours=h)
                d_lat = -(h / 24.0) * 0.6
                d_lon = (h / 24.0) * 1.1
                # Thunderstorms dissipate within 6-12 hours unless replenished by synoptic moisture
                decay = 0.90 if h == 6 else (0.45 if h == 24 else 0.15)
                track.append(TrackPoint(
                    horizon_hours=h,
                    valid_time=vt.isoformat(),
                    lat=round(lat + d_lat, 3),
                    lon=round(lon + d_lon, 3),
                    intensity=round(intensity * decay, 2),
                    wind_speed_kmh=round(base_wind * decay, 1),
                    pressure_hpa=round(base_press + (1.0 - decay) * 6.0, 1)
                ))
        else:
            event_type = "none"
            intensity = 0.05
            confidence = 0.92
            name = None
            category = "Normal Synoptic Conditions"
            track = []

        return EventSchema(
            type=event_type,
            track=track,
            intensity=round(intensity, 2),
            confidence=round(confidence, 2),
            name=name,
            category=category
        )

    # =========================================================================
    # TRACK 2: LOCAL / GRIDDED TRACK (Continuous Block-Resolution Fields)
    # =========================================================================
    def predict_gridded_fields(
        self,
        lat: float,
        lon: float,
        atmospheric_data: Dict[str, Any],
        historical_hazards: Dict[str, Any],
        elevation_m: float = 250.0,
        forecast_time: Optional[datetime] = None
    ) -> FieldsSchema:
        """
        Combines 0-6h nowcasting and 1-7d medium range model outputs to generate
        continuous physical fields with probabilistic quantile bounds.
        """
        cape = atmospheric_data.get("cape_j_kg", 1800.0)
        cin = atmospheric_data.get("cin_j_kg", 45.0)
        temp_c = atmospheric_data.get("temp_c", 31.0)
        rh = atmospheric_data.get("humidity_pct", 75.0)
        delta_tb = atmospheric_data.get("delta_tb_15m", -2.0)
        soil_moisture = atmospheric_data.get("soil_moisture_rootzone", 0.45)

        # 1. Probabilistic Rainfall Forecasting (ML model inference with physics fallback)
        p50_mm = None
        p10_mm = None
        p90_mm = None
        rainfall_prob = None

        if self.ml_rainfall_loaded:
            try:
                features = self.rainfall_meta.get("features", [])
                vt = forecast_time or datetime.now(timezone.utc)
                doy = vt.timetuple().tm_yday
                doy_sin = math.sin(2.0 * math.pi * doy / 365.25)
                doy_cos = math.cos(2.0 * math.pi * doy / 365.25)
                is_monsoon = 1.0 if (vt.month in [6, 7, 8, 9]) else 0.0

                relief_m = 35.0
                slope_deg = 1.0
                if elevation_m > 500.0:
                    relief_m = 650.0
                    slope_deg = 12.0
                elif elevation_m > 100.0:
                    relief_m = 80.0
                    slope_deg = 2.5

                # Approximate lagged rain from nowcasting inputs if not directly supplied
                rain_lag1d = float(atmospheric_data.get("rain_lag1d", 12.0 if is_monsoon else 1.0))
                rain_lag3d = float(atmospheric_data.get("rain_lag3d", 10.0 if is_monsoon else 0.8))
                rain_roll3d = float(atmospheric_data.get("rain_roll3d", (rain_lag1d + rain_lag3d) / 2.0))
                rain_roll7d = float(atmospheric_data.get("rain_roll7d", rain_roll3d * 0.95))

                nina34 = float(atmospheric_data.get("enso_index", -0.30))
                rmm1 = float(atmospheric_data.get("mjo_rmm1", 0.50))
                rmm2 = float(atmospheric_data.get("mjo_rmm2", -0.40))
                mjo_amp = float(math.sqrt(rmm1**2 + rmm2**2))
                mjo_phase = int(atmospheric_data.get("mjo_phase", 3))
                mjo_phase_sin = float(math.sin(2.0 * math.pi * (mjo_phase - 1) / 8.0))
                mjo_phase_cos = float(math.cos(2.0 * math.pi * (mjo_phase - 1) / 8.0))
                mjo_active = 1.0 if mjo_amp >= 1.0 else 0.0

                clim_daily_rain = float(atmospheric_data.get("clim_rainfall_mm", 120.0)) / 30.4
                clim_temp = float(atmospheric_data.get("temp_c", 28.0))
                clim_hum = float(atmospheric_data.get("humidity_pct", 70.0))
                clim_rainy_days = float(atmospheric_data.get("clim_rainy_days", 5.0))
                rain_anom_clim = float(rain_lag1d - clim_daily_rain)

                feat_dict = {
                    "rain_lag1d": rain_lag1d,
                    "rain_lag3d": rain_lag3d,
                    "rain_roll3d": rain_roll3d,
                    "rain_roll7d": rain_roll7d,
                    "NINA34": nina34,
                    "enso_lag1m": nina34,
                    "enso_lag3m": nina34,
                    "enso_roll3m": nina34,
                    "RMM1": rmm1,
                    "RMM2": rmm2,
                    "amplitude": mjo_amp,
                    "mjo_phase_sin": mjo_phase_sin,
                    "mjo_phase_cos": mjo_phase_cos,
                    "mjo_active": mjo_active,
                    "mjo_rmm1_lag1": rmm1,
                    "mjo_rmm2_lag1": rmm2,
                    "mjo_amp_roll7": mjo_amp,
                    "doy_sin": doy_sin,
                    "doy_cos": doy_cos,
                    "is_monsoon_season": is_monsoon,
                    "elevation_m": elevation_m,
                    "relief_m": relief_m,
                    "slope_deg": slope_deg,
                    "clim_normal_rain_daily": clim_daily_rain,
                    "clim_normal_temp": clim_temp,
                    "clim_normal_humidity": clim_hum,
                    "clim_rainy_days": clim_rainy_days,
                    "rain_anomaly_vs_clim": rain_anom_clim,
                }

                import pandas as pd
                X_df = pd.DataFrame([[feat_dict.get(c, 0.0) for c in features]], columns=features)

                ml_p50 = float(self.rf_p50.predict(X_df)[0])
                ml_p10 = float(self.rf_p10.predict(X_df)[0])
                ml_p90 = float(self.rf_p90.predict(X_df)[0])
                ml_prob = float(self.rf_clf.predict_proba(X_df)[0][1])

                p50_mm = float(np.round(np.clip(ml_p50, 0.0, 350.0), 1))
                p10_mm = float(np.round(np.clip(ml_p10, 0.0, p50_mm), 1))
                p90_mm = float(np.round(np.clip(ml_p90, p50_mm, 450.0), 1))
                rainfall_prob = float(np.round(np.clip(ml_prob, 0.05, 0.98), 2))
            except Exception:
                p50_mm = None

        # Fallback to empirical thermodynamic physics if ML model unavailable or inference failed
        if p50_mm is None:
            instability_factor = (cape / 2500.0) * (1.0 - cin / 150.0)
            convective_burst = max(0.0, -delta_tb / 10.0)
            moisture_factor = rh / 100.0

            raw_rain_prob = 0.15 + 0.45 * instability_factor + 0.25 * convective_burst + 0.15 * moisture_factor
            rainfall_prob = float(np.clip(raw_rain_prob, 0.05, 0.98))

            if rainfall_prob < 0.25:
                p50_mm = 0.0
                p10_mm = 0.0
                p90_mm = float(np.round(np.random.uniform(0.5, 3.0), 1))
            else:
                base_rain = 8.0 + 35.0 * (rainfall_prob - 0.25)
                if elevation_m > 300.0:
                    base_rain *= (1.0 + min(0.35, (elevation_m - 300.0) / 1200.0))
                p50_mm = float(np.round(base_rain, 1))
                p10_mm = float(np.round(max(0.0, p50_mm * 0.45), 1))
                p90_mm = float(np.round(p50_mm * 1.85 + 5.0, 1))

        # 2. Steadman / Rothfusz Heat Index Regression
        heat_index = self._compute_heat_index(temp_c, rh)

        # 3. Standardized Drought Index (SPEI proxy) & Soil Moisture Deficit
        # Negative indicates moisture deficit; positive indicates surplus
        normal_annual_rain = historical_hazards.get("normal_annual_rain_mm", 950.0)
        normal_daily_rain = historical_hazards.get("normal_daily_rain_mm", 4.0)
        soil_deficit = (soil_moisture - 0.40) * 4.0
        rain_anomaly = (p50_mm - normal_daily_rain) / max(2.0, normal_daily_rain * 1.5)
        drought_index = float(np.clip(soil_deficit * 0.6 + rain_anomaly * 0.4, -3.5, 3.5))

        # 4. Hydrological Flood Runoff Risk (Rainfall + Soil Saturation + Terrain)
        # SCS Curve Number proxy: high when soil is saturated and rainfall is heavy
        saturation_factor = max(0.1, soil_moisture)
        runoff_mm = max(0.0, (p50_mm - 15.0) * saturation_factor)
        flood_return_yrs = historical_hazards.get("flood_return_period_years", 6.0)
        vulnerability_weight = 1.0 / max(1.0, math.sqrt(flood_return_yrs))

        flood_risk = float(np.clip((runoff_mm / 65.0) * 0.70 + vulnerability_weight * 0.30, 0.02, 0.99))

        return FieldsSchema(
            rainfall_mm=p50_mm,
            rainfall_prob=round(rainfall_prob, 2),
            heat_index=round(heat_index, 1),
            drought_index=round(drought_index, 2),
            flood_risk=round(flood_risk, 2),
            rainfall_p10_mm=p10_mm,
            rainfall_p90_mm=p90_mm,
            temp_c=round(temp_c, 1),
            humidity_pct=round(rh, 1),
            soil_moisture_rootzone=round(soil_moisture, 2)
        )

    def _compute_heat_index(self, t_c: float, rh: float) -> float:
        """Computes Rothfusz empirical Heat Index in Celsius."""
        # Convert Celsius to Fahrenheit
        t_f = t_c * 9.0 / 5.0 + 32.0

        if t_f < 80.0:
            hi_f = 0.5 * (t_f + 61.0 + ((t_f - 68.0) * 1.2) + (rh * 0.094))
        else:
            hi_f = (
                -42.379
                + 2.04901523 * t_f
                + 10.14333127 * rh
                - 0.22475541 * t_f * rh
                - 0.00683783 * (t_f ** 2)
                - 0.05481717 * (rh ** 2)
                + 0.00122874 * (t_f ** 2) * rh
                + 0.00085282 * t_f * (rh ** 2)
                - 0.00000199 * (t_f ** 2) * (rh ** 2)
            )

        # Convert back to Celsius
        hi_c = (hi_f - 32.0) * 5.0 / 9.0
        return float(hi_c)


# Singleton instance
weather_event_model = WeatherEventModel()
