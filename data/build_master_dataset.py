"""
AryaSaarthi - Master Dataset Builder
Parses all raw datasets:
1. ENSO.csv (Niño 3.4 SST anomaly)
2. MJO.txt (RMM1, RMM2, cyclic phase, amplitude)
3. OLR data for wetbengal(1).csv (AIRS OLR)
4. humidity csv.csv (MODIS Precipitable Water Vapor)
5. SST CSV.csv (MODIS-Aqua SST)
6. circulation.csv (Surface / MSL pressure)
7. terrian of west Bengal.tiff (DEM Elevation, Slope)
8. sm_Westbengal_2020.csv (2020 District Soil Moisture)
9. DISTRICT_RAINFALL_DISTRIBUTION_COUNTRY_INDIA_cd.pdf (IMD Observed District Rainfall)
10. Historical daily gridded rainfall baseline

Builds master tables with strict no-lookahead feature engineering:
- Lagged features: T-1, T-3, T-7, T-14, T-30
- Rolling statistics (mean, std, min, max)
- Cyclic temporal features (day of year sine/cosine)
- District topographic features
"""

import os
import json
import math
import numpy as np
import pandas as pd
import tifffile
import pypdf

RAW_DIR = "/Users/adityasingh/FINAL 086/data/raw"
PROCESSED_DIR = "/Users/adityasingh/FINAL 086/data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

# --------------------------------------------------------------------------
# 1. Parse ENSO.csv
# --------------------------------------------------------------------------
def parse_enso():
    path = os.path.join(RAW_DIR, "ENSO.csv")
    print(f"Parsing {path}...")
    df = pd.read_csv(path, skiprows=1, header=None, names=["Date", "NINA34"])
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["NINA34"] = pd.to_numeric(df["NINA34"], errors="coerce")
    # Clean fill/missing value -99.99 or -9999
    df.loc[df["NINA34"] <= -90, "NINA34"] = np.nan
    df = df.dropna(subset=["Date"]).sort_values("Date").reset_index(drop=True)
    
    # Feature engineering for ENSO (monthly)
    df["enso_lag1m"] = df["NINA34"].shift(1)
    df["enso_lag3m"] = df["NINA34"].shift(3)
    df["enso_lag6m"] = df["NINA34"].shift(6)
    df["enso_lag12m"] = df["NINA34"].shift(12)
    df["enso_roll3m"] = df["NINA34"].rolling(3).mean()
    df["enso_roll6m"] = df["NINA34"].rolling(6).mean()
    df["enso_state"] = np.where(df["NINA34"] >= 0.5, "El_Nino", np.where(df["NINA34"] <= -0.5, "La_Nina", "Neutral"))
    
    # Reindex to daily by forward-filling (ENSO is monthly, published at start of month)
    daily_idx = pd.date_range(df["Date"].min(), df["Date"].max() + pd.DateOffset(months=1), freq="D")
    df_daily = df.set_index("Date").reindex(daily_idx).ffill()
    df_daily.index.name = "date"
    df_daily = df_daily.reset_index()
    print(f"  ENSO: {len(df)} monthly records -> {len(df_daily)} daily aligned records ({df['Date'].min().strftime('%Y-%m')} to {df['Date'].max().strftime('%Y-%m')})")
    return df_daily

# --------------------------------------------------------------------------
# 2. Parse MJO.txt
# --------------------------------------------------------------------------
def parse_mjo():
    path = os.path.join(RAW_DIR, "MJO.txt")
    print(f"Parsing {path}...")
    df = pd.read_csv(path, skiprows=2, header=None, sep=r"\s+")
    df = df.iloc[:, :7]
    df.columns = ["year", "month", "day", "RMM1", "RMM2", "phase", "amplitude"]
    df = df[pd.to_numeric(df["year"], errors="coerce").notnull()].copy()
    for col in ["year", "month", "day", "phase"]:
        df[col] = df[col].astype(int)
    for col in ["RMM1", "RMM2", "amplitude"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    
    # Clean missing values (999 or 1e36)
    df.loc[df["RMM1"] > 900, "RMM1"] = np.nan
    df.loc[df["RMM2"] > 900, "RMM2"] = np.nan
    df.loc[df["amplitude"] > 900, "amplitude"] = np.nan
    
    df["date"] = pd.to_datetime(df[["year", "month", "day"]], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    
    # Interpolate isolated missing values (spline/linear)
    df["RMM1"] = df["RMM1"].interpolate(method="linear")
    df["RMM2"] = df["RMM2"].interpolate(method="linear")
    df["amplitude"] = df["amplitude"].interpolate(method="linear")
    
    # Cyclic Phase Encoding (Phase 1-8 represents 360 deg equatorial wave)
    phase_rad = 2 * np.pi * (df["phase"] - 1) / 8.0
    df["mjo_phase_sin"] = np.sin(phase_rad)
    df["mjo_phase_cos"] = np.cos(phase_rad)
    df["mjo_active"] = (df["amplitude"] >= 1.0).astype(int)
    
    # Lagged features
    df["mjo_rmm1_lag1"] = df["RMM1"].shift(1)
    df["mjo_rmm1_lag3"] = df["RMM1"].shift(3)
    df["mjo_rmm1_lag7"] = df["RMM1"].shift(7)
    df["mjo_rmm2_lag1"] = df["RMM2"].shift(1)
    df["mjo_rmm2_lag3"] = df["RMM2"].shift(3)
    df["mjo_rmm2_lag7"] = df["RMM2"].shift(7)
    df["mjo_amp_roll7"] = df["amplitude"].rolling(7).mean()
    
    print(f"  MJO: {len(df)} daily records ({df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')})")
    return df

# --------------------------------------------------------------------------
# 3. Parse OLR data for wetbengal(1).csv
# --------------------------------------------------------------------------
def parse_olr():
    path = os.path.join(RAW_DIR, "OLR data for wetbengal(1).csv")
    print(f"Parsing {path}...")
    # Find header row
    with open(path, "r") as f:
        lines = [f.readline() for _ in range(15)]
    skip = 0
    for i, line in enumerate(lines):
        if line.startswith("time,"):
            skip = i
            break
            
    df = pd.read_csv(path, skiprows=skip)
    df.columns = [c.strip() for c in df.columns]
    val_col = [c for c in df.columns if c != "time"][0]
    df["date"] = pd.to_datetime(df["time"], errors="coerce")
    df["olr_wm2"] = pd.to_numeric(df[val_col], errors="coerce")
    df.loc[df["olr_wm2"] <= -9000, "olr_wm2"] = np.nan
    df = df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    
    # Fill small gaps
    df["olr_wm2"] = df["olr_wm2"].interpolate(method="linear")
    
    # Convective indicators
    # OLR < 200-220 W/m2 indicates deep tropical convection and thunderstorm activity
    df["olr_deep_convection"] = (df["olr_wm2"] < 220.0).astype(int)
    df["olr_lag1"] = df["olr_wm2"].shift(1)
    df["olr_lag3"] = df["olr_wm2"].shift(3)
    df["olr_lag7"] = df["olr_wm2"].shift(7)
    df["olr_roll3"] = df["olr_wm2"].rolling(3).mean()
    df["olr_roll7"] = df["olr_wm2"].rolling(7).mean()
    df["olr_delta_3d"] = df["olr_wm2"] - df["olr_lag3"]
    
    print(f"  OLR: {len(df)} daily records ({df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')})")
    return df[["date", "olr_wm2", "olr_deep_convection", "olr_lag1", "olr_lag3", "olr_lag7", "olr_roll3", "olr_roll7", "olr_delta_3d"]]

# --------------------------------------------------------------------------
# 4. Parse humidity csv.csv (Precipitable Water Vapor)
# --------------------------------------------------------------------------
def parse_humidity():
    path = os.path.join(RAW_DIR, "humidity csv.csv")
    print(f"Parsing {path}...")
    with open(path, "r") as f:
        lines = [f.readline() for _ in range(15)]
    skip = 0
    for i, line in enumerate(lines):
        if line.startswith("time,"):
            skip = i
            break
            
    df = pd.read_csv(path, skiprows=skip)
    df.columns = [c.strip() for c in df.columns]
    val_col = [c for c in df.columns if c != "time"][0]
    df["date"] = pd.to_datetime(df["time"], errors="coerce")
    df["precipitable_water_cm"] = pd.to_numeric(df[val_col], errors="coerce")
    df.loc[df["precipitable_water_cm"] <= -9000, "precipitable_water_cm"] = np.nan
    df = df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    df["precipitable_water_cm"] = df["precipitable_water_cm"].interpolate(method="linear")
    
    # Feature engineering
    df["pwv_lag1"] = df["precipitable_water_cm"].shift(1)
    df["pwv_lag3"] = df["precipitable_water_cm"].shift(3)
    df["pwv_lag7"] = df["precipitable_water_cm"].shift(7)
    df["pwv_roll3"] = df["precipitable_water_cm"].rolling(3).mean()
    df["pwv_roll7"] = df["precipitable_water_cm"].rolling(7).mean()
    df["pwv_high_moisture"] = (df["precipitable_water_cm"] >= 3.5).astype(int)
    
    print(f"  Precipitable Water: {len(df)} daily records ({df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')})")
    return df[["date", "precipitable_water_cm", "pwv_lag1", "pwv_lag3", "pwv_lag7", "pwv_roll3", "pwv_roll7", "pwv_high_moisture"]]

# --------------------------------------------------------------------------
# 5. Parse SST CSV.csv
# --------------------------------------------------------------------------
def parse_sst():
    path = os.path.join(RAW_DIR, "SST CSV.csv")
    print(f"Parsing {path}...")
    with open(path, "r") as f:
        lines = [f.readline() for _ in range(15)]
    skip = 0
    for i, line in enumerate(lines):
        if line.startswith("time,"):
            skip = i
            break
            
    df = pd.read_csv(path, skiprows=skip)
    df.columns = [c.strip() for c in df.columns]
    val_col = [c for c in df.columns if c != "time"][0]
    df["date"] = pd.to_datetime(df["time"], errors="coerce")
    df["sst_c"] = pd.to_numeric(df[val_col], errors="coerce")
    df.loc[df["sst_c"] <= -9000, "sst_c"] = np.nan
    df = df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    
    # Interpolate 8-daily to daily
    daily_idx = pd.date_range(df["date"].min(), df["date"].max(), freq="D")
    df_daily = df.set_index("date")[["sst_c"]].reindex(daily_idx).interpolate(method="time").reset_index()
    df_daily.columns = ["date", "sst_c"]
    df_daily["sst_lag7"] = df_daily["sst_c"].shift(7)
    df_daily["sst_roll14"] = df_daily["sst_c"].rolling(14).mean()
    
    print(f"  SST: {len(df)} 8-daily records -> {len(df_daily)} interpolated daily records")
    return df_daily

# --------------------------------------------------------------------------
# 6. Parse circulation.csv
# --------------------------------------------------------------------------
def parse_circulation():
    path = os.path.join(RAW_DIR, "circulation.csv")
    print(f"Parsing {path}...")
    with open(path, "r") as f:
        lines = f.readlines()
    
    skip = 0
    for i, l in enumerate(lines):
        if l.startswith("time,"):
            skip = i
            break
            
    df = pd.read_csv(path, skiprows=skip)
    df.columns = [c.strip() for c in df.columns]
    df["date"] = pd.to_datetime(df["time"], errors="coerce")
    val_col = [c for c in df.columns if c not in ["time", "date"]][0]
    df["msl_pressure_hpa"] = pd.to_numeric(df[val_col], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    
    df["press_lag1"] = df["msl_pressure_hpa"].shift(1)
    df["press_lag3"] = df["msl_pressure_hpa"].shift(3)
    df["press_delta_24h"] = df["msl_pressure_hpa"] - df["press_lag1"]
    
    print(f"  Circulation: {len(df)} daily pressure records ({df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')})")
    return df[["date", "msl_pressure_hpa", "press_lag1", "press_lag3", "press_delta_24h"]]

# --------------------------------------------------------------------------
# 7. Parse terrian of west Bengal.tiff (DEM Extraction)
# --------------------------------------------------------------------------
def extract_district_topography():
    topo_cache_path = os.path.join(PROCESSED_DIR, "west_bengal_district_topography.json")
    if os.path.exists(topo_cache_path):
        print(f"Loading cached district topography from {topo_cache_path}...")
        with open(topo_cache_path, "r") as f:
            return json.load(f)

    path = os.path.join(RAW_DIR, "terrian of west Bengal.tiff")
    if not os.path.exists(path):
        print(f"Warning: {path} not found and no cache exists. Returning default topography.")
        return {}
    print(f"Parsing {path} (160 MB GeoTIFF)...")
    
    page = tifffile.TiffFile(path).pages[0]
    arr = page.asarray()
    scale = 0.0008333333333333334
    lon_min, lat_max = 85.5, 27.5
    
    # 23 Districts of West Bengal with representative center coordinates
    wb_districts = {
        "BIRBHUM": (23.8400, 87.6100),
        "BANKURA": (23.2300, 87.0800),
        "BARDDHAMAN": (23.2400, 87.8600),
        "PURBA BARDHAMAN": (23.2400, 87.8600),
        "PASCHIM BARDHAMAN": (23.6800, 86.9800),
        "DARJILING": (27.0410, 88.2663),
        "KALIMPONG": (27.0600, 88.4700),
        "JALPAIGURI": (26.5414, 88.7195),
        "ALIPURDUAR": (26.4900, 89.5200),
        "KOCH BIHAR": (26.3200, 89.4500),
        "MALDAH": (25.0100, 88.1400),
        "UTTAR DINAJPUR": (25.6200, 88.1200),
        "DAKSHIN DINAJPUR": (25.2200, 88.7600),
        "MURSHIDABAD": (24.1800, 88.2700),
        "NADIA": (23.4700, 88.5500),
        "PURULIYA": (23.3321, 86.3652),
        "HUGLI": (22.9000, 88.3900),
        "HAORA": (22.5800, 88.3200),
        "KOLKATA": (22.5726, 88.3639),
        "NORTH 24 PARGANAS": (22.7200, 88.4800),
        "SOUTH 24 PARGANAS": (22.1800, 88.5500),
        "PASCHIM MEDINIPUR": (22.4200, 87.3200),
        "PURBA MEDINIPUR": (21.9400, 87.7700),
        "JHARGRAM": (22.4500, 86.9800)
    }
    
    topo_dict = {}
    radius_px = 30  # ~2.5 km box around centroid to compute mean and slope variance
    
    for dist_name, (lat, lon) in wb_districts.items():
        r = int(round((lat_max - lat) / scale))
        c = int(round((lon - lon_min) / scale))
        
        r_min = max(0, r - radius_px)
        r_max = min(arr.shape[0], r + radius_px)
        c_min = max(0, c - radius_px)
        c_max = min(arr.shape[1], c + radius_px)
        
        sub = arr[r_min:r_max, c_min:c_max]
        valid_mask = (sub > -100) & (sub < 9000)
        valid = sub[valid_mask]
        
        dx_m = scale * 111320.0
        if len(valid) > 0 and sub.shape[0] > 2 and sub.shape[1] > 2:
            elev_mean = float(np.mean(valid))
            elev_min = float(np.min(valid))
            elev_max = float(np.max(valid))
            relief = elev_max - elev_min
            
            # Genuine 2D topographic slope in degrees
            dy, dx = np.gradient(sub, dx_m)
            slope_deg_grid = np.degrees(np.arctan(np.sqrt(dx**2 + dy**2)))
            slope_deg = float(np.nanmean(slope_deg_grid[valid_mask]))
        else:
            elev_mean = 50.0
            relief = 10.0
            slope_deg = 0.5
            
        topo_dict[dist_name] = {
            "lat": lat,
            "lon": lon,
            "elevation_m": round(elev_mean, 1),
            "relief_m": round(relief, 1),
            "slope_deg": round(slope_deg, 2)
        }
        
    print(f"  Topography extracted for {len(topo_dict)} West Bengal districts:")
    for d in ["DARJILING", "PURULIYA", "BIRBHUM", "KOLKATA", "PURBA MEDINIPUR"]:
        t = topo_dict[d]
        print(f"    {d}: Elev={t['elevation_m']}m, Relief={t['relief_m']}m, Slope={t['slope_deg']}°")
        
    return topo_dict

# --------------------------------------------------------------------------
# 8. Parse sm_Westbengal_2020.csv
# --------------------------------------------------------------------------
def parse_soil_moisture_wb():
    path = os.path.join(RAW_DIR, "sm_Westbengal_2020.csv")
    print(f"Parsing {path}...")
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["district"] = df["DistrictName"].str.upper().str.strip()
    
    # Standardize district names
    name_map = {
        "DARJEELING": "DARJILING",
        "HOOGHLY": "HUGLI",
        "HOWRAH": "HAORA",
        "MALDA": "MALDAH",
        "PURULIA": "PURULIYA",
        "BURDWAN": "BARDDHAMAN",
        "COOCHBEHAR": "KOCH BIHAR"
    }
    df["district"] = df["district"].replace(name_map)
    
    val_level = "Average Soilmoisture Level (at 15cm)"
    val_vol = "Average SoilMoisture Volume (at 15cm)"
    val_pct = "Aggregate Soilmoisture Percentage (at 15cm)"
    val_vol_pct = "Volume Soilmoisture percentage (at 15cm)"
    
    df["sm_level_15cm"] = pd.to_numeric(df[val_level], errors="coerce")
    df["sm_volume_15cm"] = pd.to_numeric(df[val_vol], errors="coerce")
    df["sm_pct_15cm"] = pd.to_numeric(df[val_pct], errors="coerce")
    df["sm_vol_pct_15cm"] = pd.to_numeric(df[val_vol_pct], errors="coerce")
    
    df = df.dropna(subset=["date", "district"]).sort_values(["district", "date"]).reset_index(drop=True)
    
    # Lagged soil moisture features per district
    df["sm_pct_lag1"] = df.groupby("district")["sm_pct_15cm"].shift(1)
    df["sm_pct_lag3"] = df.groupby("district")["sm_pct_15cm"].shift(3)
    df["sm_pct_lag7"] = df.groupby("district")["sm_pct_15cm"].shift(7)
    df["sm_pct_roll7"] = df.groupby("district")["sm_pct_15cm"].transform(lambda s: s.rolling(7).mean())
    
    # Soil moisture deficit: (sm - mean) / std per district
    dist_means = df.groupby("district")["sm_pct_15cm"].transform("mean")
    dist_stds = df.groupby("district")["sm_pct_15cm"].transform("std").replace(0, 1.0)
    df["sm_deficit_zscore"] = (df["sm_pct_15cm"] - dist_means) / dist_stds
    
    print(f"  Soil Moisture WB: {len(df)} records across {df['district'].nunique()} districts in 2020")
    return df

# --------------------------------------------------------------------------
# 9. Parse DISTRICT_RAINFALL_DISTRIBUTION_COUNTRY_INDIA_cd.pdf
# --------------------------------------------------------------------------
def parse_imd_district_rainfall_pdf():
    path = os.path.join(RAW_DIR, "DISTRICT_RAINFALL_DISTRIBUTION_COUNTRY_INDIA_cd.pdf")
    print(f"Parsing {path}...")
    reader = pypdf.PdfReader(path)
    
    records = []
    # Search all pages for West Bengal entries
    for p_idx, page in enumerate(reader.pages):
        text = page.extract_text()
        if "WEST BENGAL" in text:
            lines = text.split("\n")
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 9 and parts[0].isdigit():
                    # E.g. 2 BIRBHUM 37.9 11.1 242% LE 938 1082.9 -13% N
                    dist_name = parts[1].upper()
                    try:
                        day_act = float(parts[2])
                        day_norm = float(parts[3])
                        day_dep_str = parts[4].replace("%", "")
                        day_dep = float(day_dep_str)
                        day_cat = parts[5]
                        cum_act = float(parts[6])
                        cum_norm = float(parts[7])
                        cum_dep_str = parts[8].replace("%", "")
                        cum_dep = float(cum_dep_str)
                        cum_cat = parts[9] if len(parts) > 9 else "N"
                        
                        records.append({
                            "district": dist_name,
                            "obs_date": "2026-09-24",
                            "imd_day_actual_mm": day_act,
                            "imd_day_normal_mm": day_norm,
                            "imd_day_departure_pct": day_dep,
                            "imd_day_category": day_cat,
                            "imd_cumulative_actual_mm": cum_act,
                            "imd_cumulative_normal_mm": cum_norm,
                            "imd_cumulative_departure_pct": cum_dep,
                            "imd_cumulative_category": cum_cat
                        })
                    except Exception:
                        continue
                        
    df_imd = pd.DataFrame(records).drop_duplicates(subset=["district"]).reset_index(drop=True)
    print(f"  IMD PDF: Parsed {len(df_imd)} West Bengal district records for 2026-09-24")
    return df_imd

# --------------------------------------------------------------------------
# 10. Load Existing Historical Gridded Rainfall Baseline
# --------------------------------------------------------------------------
def load_historical_gridded_rainfall():
    path = os.path.join(PROCESSED_DIR, "block_agromet_combined.parquet")
    if not os.path.exists(path):
        path = os.path.join(PROCESSED_DIR, "imd_chirps_block_rainfall.parquet")
        
    if os.path.exists(path):
        print(f"Loading historical gridded rainfall from {path}...")
        df = pd.read_parquet(path)
        agg_dict = {"rainfall_mm": "mean"}
        for col in ["temp_max_c", "soil_wetness_rootzone", "solar_radiation_mj"]:
            if col in df.columns:
                agg_dict[col] = "mean"
                
        df_dist = df.groupby(["date", "district"]).agg(agg_dict).reset_index()
        df_dist["district"] = df_dist["district"].str.upper().str.strip()
        print(f"  Historical Gridded Panel: {len(df_dist)} records across {df_dist['district'].nunique()} districts")
        return df_dist
    return None

# --------------------------------------------------------------------------
# 11. Assemble Master Spatiotemporal Dataset
# --------------------------------------------------------------------------
def assemble_master_dataset():
    print("\n" + "="*60)
    print("ASSEMBLING MASTER SPATIOTEMPORAL DATASET")
    print("="*60)
    
    enso_df = parse_enso()
    mjo_df = parse_mjo()
    olr_df = parse_olr()
    hum_df = parse_humidity()
    sst_df = parse_sst()
    circ_df = parse_circulation()
    topo_dict = extract_district_topography()
    sm_df = parse_soil_moisture_wb()
    imd_pdf_df = parse_imd_district_rainfall_pdf()
    hist_rain_df = load_historical_gridded_rainfall()
    
    # Save parsed clean components to processed dir
    enso_df.to_parquet(os.path.join(PROCESSED_DIR, "enso_daily_aligned.parquet"))
    mjo_df.to_parquet(os.path.join(PROCESSED_DIR, "mjo_features_clean.parquet"))
    olr_df.to_parquet(os.path.join(PROCESSED_DIR, "airs_olr_daily.parquet"))
    hum_df.to_parquet(os.path.join(PROCESSED_DIR, "modis_pwv_daily.parquet"))
    sst_df.to_parquet(os.path.join(PROCESSED_DIR, "modis_sst_daily.parquet"))
    circ_df.to_parquet(os.path.join(PROCESSED_DIR, "circulation_pressure_daily.parquet"))
    sm_df.to_parquet(os.path.join(PROCESSED_DIR, "soil_moisture_wb_2020.parquet"))
    imd_pdf_df.to_parquet(os.path.join(PROCESSED_DIR, "imd_district_rainfall_20260924.parquet"))
    
    with open(os.path.join(PROCESSED_DIR, "west_bengal_district_topography.json"), "w") as f:
        json.dump(topo_dict, f, indent=2)
        
    print("\nMerging teleconnection and atmospheric driver cubes (2000-2026)...")
    
    # Construct base date spine for 2000 to 2026
    spine = pd.DataFrame({"date": pd.date_range("2000-01-01", "2026-09-24", freq="D")})
    
    # Merge teleconnections
    drivers = spine.merge(enso_df[["date", "NINA34", "enso_lag1m", "enso_lag3m", "enso_roll3m", "enso_state"]], on="date", how="left")
    drivers = drivers.merge(mjo_df[["date", "RMM1", "RMM2", "amplitude", "mjo_phase_sin", "mjo_phase_cos", "mjo_active", "mjo_rmm1_lag1", "mjo_rmm2_lag1", "mjo_amp_roll7"]], on="date", how="left")
    drivers = drivers.merge(olr_df, on="date", how="left")
    drivers = drivers.merge(hum_df, on="date", how="left")
    drivers = drivers.merge(sst_df, on="date", how="left")
    drivers = drivers.merge(circ_df, on="date", how="left")
    
    # Cyclical day of year
    doy = drivers["date"].dt.dayofyear
    drivers["doy_sin"] = np.sin(2 * np.pi * doy / 365.25)
    drivers["doy_cos"] = np.cos(2 * np.pi * doy / 365.25)
    drivers["is_monsoon_season"] = drivers["date"].dt.month.isin([6, 7, 8, 9]).astype(int)
    
    # If historical gridded rainfall exists, combine into panel per district
    master_panel_rows = []
    
    if hist_rain_df is not None:
        # Cross join drivers with districts
        districts = sorted(list(topo_dict.keys()))
        print(f"Creating district panel for {len(districts)} districts across historical timeline...")
        
        # Merge hist_rain_df with drivers
        merged_panel = hist_rain_df.merge(drivers, on="date", how="inner")
        
        # Attach topography
        merged_panel["elevation_m"] = merged_panel["district"].map(lambda d: topo_dict.get(d, {}).get("elevation_m", 50.0))
        merged_panel["relief_m"] = merged_panel["district"].map(lambda d: topo_dict.get(d, {}).get("relief_m", 15.0))
        merged_panel["slope_deg"] = merged_panel["district"].map(lambda d: topo_dict.get(d, {}).get("slope_deg", 0.5))
        
        # Add target variables (No lookahead: next day rainfall, next 3-day accumulated rainfall)
        merged_panel = merged_panel.sort_values(["district", "date"]).reset_index(drop=True)
        merged_panel["target_rain_next_1d"] = merged_panel.groupby("district")["rainfall_mm"].shift(-1)
        merged_panel["target_rain_next_3d"] = (
            merged_panel.groupby("district")["rainfall_mm"].shift(-1) +
            merged_panel.groupby("district")["rainfall_mm"].shift(-2) +
            merged_panel.groupby("district")["rainfall_mm"].shift(-3)
        )
        merged_panel["target_rain_event_next_1d"] = (merged_panel["target_rain_next_1d"] >= 2.5).astype(float)
        merged_panel["target_heavy_rain_next_1d"] = (merged_panel["target_rain_next_1d"] >= 64.5).astype(float)
        
        # Lagged rainfall predictors (Strictly at or before T)
        merged_panel["rain_lag1d"] = merged_panel.groupby("district")["rainfall_mm"].shift(1)
        merged_panel["rain_lag3d"] = merged_panel.groupby("district")["rainfall_mm"].shift(3)
        merged_panel["rain_roll3d"] = merged_panel.groupby("district")["rainfall_mm"].transform(lambda s: s.rolling(3).mean())
        merged_panel["rain_roll7d"] = merged_panel.groupby("district")["rainfall_mm"].transform(lambda s: s.rolling(7).mean())
        
        master_panel_path = os.path.join(PROCESSED_DIR, "west_bengal_master_spatiotemporal.parquet")
        merged_panel.to_parquet(master_panel_path)
        print(f"Master spatiotemporal dataset constructed: {len(merged_panel)} records -> {master_panel_path}")
        
    # Construct 2020 West Bengal Soil Moisture Panel with teleconnections & topography
    sm_panel = sm_df.merge(drivers, on="date", how="left")
    sm_panel["elevation_m"] = sm_panel["district"].map(lambda d: topo_dict.get(d, {}).get("elevation_m", 50.0))
    sm_panel["relief_m"] = sm_panel["district"].map(lambda d: topo_dict.get(d, {}).get("relief_m", 15.0))
    sm_panel["slope_deg"] = sm_panel["district"].map(lambda d: topo_dict.get(d, {}).get("slope_deg", 0.5))
    sm_panel = sm_panel.sort_values(["district", "date"]).reset_index(drop=True)
    sm_panel["target_sm_pct_next_1d"] = sm_panel.groupby("district")["sm_pct_15cm"].shift(-1)
    sm_panel["target_sm_pct_next_3d"] = sm_panel.groupby("district")["sm_pct_15cm"].shift(-3)
    sm_panel["target_sm_deficit_next_1d"] = sm_panel.groupby("district")["sm_deficit_zscore"].shift(-1)
    sm_panel_path = os.path.join(PROCESSED_DIR, "west_bengal_soil_moisture_panel_2020.parquet")
    sm_panel.to_parquet(sm_panel_path)
    print(f"West Bengal 2020 Soil Moisture Panel constructed: {len(sm_panel)} records -> {sm_panel_path}")

    drivers_path = os.path.join(PROCESSED_DIR, "teleconnection_satellite_drivers_daily.parquet")
    drivers.to_parquet(drivers_path)
    print(f"Drivers cube saved: {len(drivers)} daily records -> {drivers_path}")
    print("Dataset construction complete.")

if __name__ == "__main__":
    assemble_master_dataset()
