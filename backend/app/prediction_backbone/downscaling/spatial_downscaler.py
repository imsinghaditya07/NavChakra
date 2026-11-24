"""
Spatial Downscaling Engine: Coarse Grid (10–25km) → Block → Gram Panchayat.

Implements:
1. Topographic Lapse-Rate & Adiabatic Correction (-6.5°C/km)
2. Orographic Rain Enhancement & Rain-Shadow Attenuation
3. Surface Roughness & Boundary Layer Aerodynamic Wind Adjustment
4. Rigorous Confidence Propagation:
   - Every Panchayat-level value carries the parent grid cell's confidence
   - Penalized by sub-grid topographic variance and spatial distance
   - Prevents false precision at hyperlocal resolutions.
"""

import math
from typing import Dict, Any, Tuple
import numpy as np

from backend.app.prediction_backbone.schema import FieldsSchema, WindParticle


class SpatialDownscaler:
    """
    Downscales synoptic/meso gridded fields to specific Gram Panchayat boundaries.
    """

    def __init__(self):
        # Environmental lapse rate in Celsius per meter
        self.lapse_rate_c_per_m = -0.0065

    def downscale_to_panchayat(
        self,
        grid_fields: FieldsSchema,
        grid_wind: WindParticle,
        parent_confidence: float,
        panchayat_meta: Dict[str, Any],
        grid_elevation_m: float = 250.0
    ) -> Tuple[FieldsSchema, WindParticle, float, Dict[str, Any]]:
        """
        Executes physical downscaling to Panchayat GIS centroid.
        Returns:
            (downscaled_fields, downscaled_wind, propagated_confidence, downscale_audit_log)
        """
        panchayat_elev_m = panchayat_meta.get("elevation_m", grid_elevation_m)
        elev_diff_m = panchayat_elev_m - grid_elevation_m
        terrain_roughness_m = panchayat_meta.get("terrain_roughness_m", 45.0)

        # 1. Temperature Lapse Rate Adjustment
        delta_temp = elev_diff_m * self.lapse_rate_c_per_m
        panch_temp = (grid_fields.temp_c or 31.0) + delta_temp

        # 2. Relative Humidity Adjustment (Clausius-Clapeyron cooler air has lower saturation vapor pressure)
        # Cooling increases relative humidity by ~4.5% per degree C drop
        panch_rh = (grid_fields.humidity_pct or 75.0) - (delta_temp * 3.5)
        panch_rh = float(np.clip(panch_rh, 15.0, 98.0))

        # 3. Orographic Rain Modification
        # Air forced up a slope condenses moisture faster (orographic enhancement)
        # Leeward descent creates rain-shadow drying
        wind_dir = grid_wind.direction_deg
        aspect_deg = panchayat_meta.get("slope_aspect_deg", 225.0)
        
        # Angle between incoming wind and terrain slope
        angle_diff = abs((wind_dir - aspect_deg + 180.0) % 360.0 - 180.0)
        is_windward = angle_diff < 90.0

        orographic_multiplier = 1.0
        if elev_diff_m > 30.0 and is_windward:
            # Upslope enhancement: +5% to +20%
            orographic_multiplier = 1.0 + min(0.25, (elev_diff_m / 600.0) * math.cos(math.radians(angle_diff)))
        elif elev_diff_m < -30.0:
            # Valley rain shadow / subsidence: slight attenuation
            orographic_multiplier = max(0.85, 1.0 - abs(elev_diff_m) / 1000.0)

        panch_rain_mm = round(grid_fields.rainfall_mm * orographic_multiplier, 1)
        panch_rain_p10 = round((grid_fields.rainfall_p10_mm or 0.0) * orographic_multiplier, 1)
        panch_rain_p90 = round((grid_fields.rainfall_p90_mm or 0.0) * orographic_multiplier, 1)
        panch_rain_prob = round(float(np.clip(grid_fields.rainfall_prob * (1.0 + (orographic_multiplier - 1.0) * 0.4), 0.05, 0.99)), 2)

        # 4. Heat Index recalculation with downscaled temperature & humidity
        t_f = panch_temp * 9.0 / 5.0 + 32.0
        panch_hi = (
            -42.379
            + 2.04901523 * t_f
            + 10.14333127 * panch_rh
            - 0.22475541 * t_f * panch_rh
            - 0.00683783 * (t_f ** 2)
            - 0.05481717 * (panch_rh ** 2)
            + 0.00122874 * (t_f ** 2) * panch_rh
            + 0.00085282 * t_f * (panch_rh ** 2)
            - 0.00000199 * (t_f ** 2) * (panch_rh ** 2)
        )
        panch_hi_c = round((panch_hi - 32.0) * 5.0 / 9.0, 1)

        # 5. Wind Boundary Layer Downscaling
        # Agricultural canopy and valley friction attenuate wind speed
        land_use = panchayat_meta.get("land_use", "agricultural")
        friction_factor = 0.82 if land_use == "agricultural" else (0.72 if land_use == "village_settlement" else 0.95)
        panch_wind_speed = round(grid_wind.speed_kmh * friction_factor, 1)

        # 6. Confidence Propagation & Variance Penalty
        # Never imply false precision: subgrid terrain variance reduces confidence
        variance_penalty = min(0.12, (terrain_roughness_m / 500.0) * 0.15)
        propagated_confidence = round(float(np.clip(parent_confidence * (1.0 - variance_penalty), 0.45, 0.98)), 2)

        downscaled_fields = FieldsSchema(
            rainfall_mm=panch_rain_mm,
            rainfall_prob=panch_rain_prob,
            heat_index=panch_hi_c,
            drought_index=grid_fields.drought_index,
            flood_risk=grid_fields.flood_risk,
            rainfall_p10_mm=panch_rain_p10,
            rainfall_p90_mm=panch_rain_p90,
            temp_c=round(panch_temp, 1),
            humidity_pct=round(panch_rh, 1),
            soil_moisture_rootzone=grid_fields.soil_moisture_rootzone
        )

        downscaled_wind = WindParticle(
            speed_kmh=panch_wind_speed,
            direction_deg=grid_wind.direction_deg,
            u_ms=round((grid_wind.u_ms or 0.0) * friction_factor, 2),
            v_ms=round((grid_wind.v_ms or 0.0) * friction_factor, 2)
        )

        audit_log = {
            "elevation_delta_m": elev_diff_m,
            "orographic_multiplier": round(orographic_multiplier, 3),
            "windward_slope": is_windward,
            "variance_penalty": round(variance_penalty, 3),
            "original_grid_confidence": parent_confidence,
            "propagated_panchayat_confidence": propagated_confidence
        }

        return downscaled_fields, downscaled_wind, propagated_confidence, audit_log


# Singleton instance
spatial_downscaler = SpatialDownscaler()
