"""
AryaSaarthi - Comprehensive Data Audit Script
Inspects all 19 actual raw data files in data/raw/.
Extracts:
- format, file size, record count, column count, variables, units
- time range, frequency, spatial bounds, resolution, CRS
- missing values, duplicate records, data source, ML role
"""

import os
import json
import glob
import pandas as pd
import numpy as np
import tifffile
import pypdf
from PIL import Image

RAW_DIR = "/Users/adityasingh/FINAL 086/data/raw"

def audit_file(filepath):
    filename = os.path.basename(filepath)
    size_bytes = os.path.getsize(filepath)
    ext = os.path.splitext(filename)[1].lower()
    
    info = {
        "filename": filename,
        "size_bytes": size_bytes,
        "format": ext,
        "status": "OK",
        "metadata": {},
        "summary": {}
    }
    
    try:
        if ext == ".txt":
            # Likely MJO.txt
            with open(filepath, "r", errors="ignore") as f:
                first_lines = [f.readline() for _ in range(10)]
            info["first_10_lines"] = [l.strip() for l in first_lines]
            
            # Parse MJO table
            # format has 2 header lines
            df = pd.read_csv(filepath, skiprows=2, header=None, delim_whitespace=True)
            # year, month, day, RMM1, RMM2, phase, amplitude, notes
            df = df.iloc[:, :7]
            df.columns = ["year", "month", "day", "RMM1", "RMM2", "phase", "amplitude"]
            # Filter valid rows where year is integer
            df = df[pd.to_numeric(df["year"], errors="coerce").notnull()].copy()
            for col in ["year", "month", "day", "phase"]:
                df[col] = df[col].astype(int)
            for col in ["RMM1", "RMM2", "amplitude"]:
                df[col] = pd.to_numeric(df[col], errors="coerce")
            
            # Missing value check: 999 or 1e36
            df.loc[df["RMM1"] > 900, "RMM1"] = np.nan
            df.loc[df["RMM2"] > 900, "RMM2"] = np.nan
            df.loc[df["amplitude"] > 900, "amplitude"] = np.nan
            
            dates = pd.to_datetime(df[["year", "month", "day"]], errors="coerce")
            df["date"] = dates
            
            info["num_records"] = len(df)
            info["num_columns"] = len(df.columns)
            info["columns"] = list(df.columns)
            info["time_min"] = str(df["date"].min())
            info["time_max"] = str(df["date"].max())
            info["missing_count"] = int(df.isna().sum().sum())
            info["duplicates"] = int(df.duplicated(subset=["date"]).sum())
            info["frequency"] = "Daily"
            info["spatial_coverage"] = "Global Tropics (MJO RMM1/RMM2)"
            info["variables"] = "RMM1, RMM2, phase (1-8), amplitude"
            info["units"] = "Standardized EOF index"
            info["role"] = "Teleconnection Feature"
            
        elif ext == ".csv":
            # Inspect first 15 lines to identify metadata headers
            with open(filepath, "r", errors="ignore") as f:
                head = [f.readline().strip() for _ in range(15)]
            
            meta_lines = []
            header_idx = 0
            for i, line in enumerate(head):
                if line.startswith("Title:") or line.startswith("User ") or line.startswith("Data ") or line.startswith("URL ") or line.startswith("Fill Value"):
                    meta_lines.append(line)
                    header_idx = i + 1
            
            info["metadata"]["detected_meta"] = meta_lines
            
            # Special handling by filename
            if "ENSO" in filename:
                # First line might have metadata: Date, NINA34 missing value -99.99 https://psl.noaa.gov/data/timeseries/month/
                df = pd.read_csv(filepath, skiprows=1, header=None, names=["Date", "NINA34"])
                df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
                df["NINA34"] = pd.to_numeric(df["NINA34"], errors="coerce")
                # Missing value is -99.99 or -9999
                df.loc[df["NINA34"] <= -90, "NINA34"] = np.nan
                info["num_records"] = len(df)
                info["columns"] = list(df.columns)
                info["time_min"] = str(df["Date"].min())
                info["time_max"] = str(df["Date"].max())
                info["missing_count"] = int(df.isna().sum().sum())
                info["duplicates"] = int(df.duplicated(subset=["Date"]).sum())
                info["frequency"] = "Monthly"
                info["spatial_coverage"] = "Niño 3.4 Region (5N-5S, 170W-120W)"
                info["variables"] = "Niño 3.4 SST anomaly index"
                info["units"] = "°C anomaly"
                info["role"] = "Teleconnection Feature"
                
            elif "OLR" in filename:
                df = pd.read_csv(filepath, skiprows=header_idx)
                df.columns = [c.strip() for c in df.columns]
                # date, mean_AIRS3STD_7_0_OLR_A
                val_col = [c for c in df.columns if c != "time"][0]
                df["time"] = pd.to_datetime(df["time"], errors="coerce")
                df[val_col] = pd.to_numeric(df[val_col], errors="coerce")
                df.loc[df[val_col] <= -9000, val_col] = np.nan
                info["num_records"] = len(df)
                info["columns"] = list(df.columns)
                info["time_min"] = str(df["time"].min())
                info["time_max"] = str(df["time"].max())
                info["missing_count"] = int(df.isna().sum().sum())
                info["duplicates"] = int(df.duplicated(subset=["time"]).sum())
                info["frequency"] = "Daily"
                info["spatial_coverage"] = "West Bengal Bounding Box (85.5-89.5E, 21.5-27.5N)"
                info["variables"] = "Outgoing Longwave Radiation (Daytime Ascending, AIRS)"
                info["units"] = "W/m²"
                info["role"] = "Convective / Cloud Activity Feature"
                
            elif "humidity" in filename:
                df = pd.read_csv(filepath, skiprows=header_idx)
                df.columns = [c.strip() for c in df.columns]
                val_col = [c for c in df.columns if c != "time"][0]
                df["time"] = pd.to_datetime(df["time"], errors="coerce")
                df[val_col] = pd.to_numeric(df[val_col], errors="coerce")
                df.loc[df[val_col] <= -9000, val_col] = np.nan
                info["num_records"] = len(df)
                info["columns"] = list(df.columns)
                info["time_min"] = str(df["time"].min())
                info["time_max"] = str(df["time"].max())
                info["missing_count"] = int(df.isna().sum().sum())
                info["duplicates"] = int(df.duplicated(subset=["time"]).sum())
                info["frequency"] = "Daily"
                info["spatial_coverage"] = "West Bengal Bounding Box (85.5-89.5E, 21.5-27.5N)"
                info["variables"] = "Precipitable Water Vapor (IR Retrieval Surface to 680mb, MODIS MOD08_D3)"
                info["units"] = "cm (liquid water equivalent)"
                info["role"] = "Atmospheric Moisture Feature"
                
            elif "SST" in filename:
                df = pd.read_csv(filepath, skiprows=header_idx)
                df.columns = [c.strip() for c in df.columns]
                val_col = [c for c in df.columns if c != "time"][0]
                df["time"] = pd.to_datetime(df["time"], errors="coerce")
                df[val_col] = pd.to_numeric(df[val_col], errors="coerce")
                df.loc[df[val_col] <= -9000, val_col] = np.nan
                info["num_records"] = len(df)
                info["columns"] = list(df.columns)
                info["time_min"] = str(df["time"].min())
                info["time_max"] = str(df["time"].max())
                info["missing_count"] = int(df.isna().sum().sum())
                info["duplicates"] = int(df.duplicated(subset=["time"]).sum())
                info["frequency"] = "8-Daily"
                info["spatial_coverage"] = "Bay of Bengal offshore West Bengal (85.5-89.9E, 21.0-27.5N)"
                info["variables"] = "Sea Surface Temperature at 11 microns (MODIS-Aqua L3m)"
                info["units"] = "°C"
                info["role"] = "Oceanic / Thermal Feature"
                
            elif "ERA5" in filename:
                # Inspect structure: multi-table CSV (coords header, hourly table, daily table)
                with open(filepath, "r") as f:
                    content = f.read()
                sections = content.strip().split("\n\n")
                info["metadata"]["sections_count"] = len(sections)
                # First section: latitude,longitude,elevation
                s1_lines = sections[0].strip().split("\n")
                info["metadata"]["location_metadata"] = s1_lines
                # Second section: hourly observations
                s2_io = pd.compat.StringIO(sections[1]) if hasattr(pd.compat, "StringIO") else pd.io.common.StringIO(sections[1])
                df_hourly = pd.read_csv(s2_io)
                info["hourly_records"] = len(df_hourly)
                info["hourly_columns"] = list(df_hourly.columns)
                info["time_min"] = str(df_hourly["time"].min())
                info["time_max"] = str(df_hourly["time"].max())
                # Third section: daily aggregations
                if len(sections) > 2:
                    s3_io = pd.compat.StringIO(sections[2]) if hasattr(pd.compat, "StringIO") else pd.io.common.StringIO(sections[2])
                    df_daily = pd.read_csv(s3_io)
                    info["daily_records"] = len(df_daily)
                    info["daily_columns"] = list(df_daily.columns)
                info["frequency"] = "Hourly and Daily"
                info["spatial_coverage"] = "Single Lat/Lon: 28.576N, 77.187E (Delhi Safdarjung area), Elev 214m"
                info["variables"] = "T2m, RH2m, DewPoint, Pressure MSL, Surface Pressure, Wind Speed/Dir, Precipitation, Soil Temp, Soil Moisture"
                info["units"] = "°C, %, hPa, km/h, mm, m³/m³"
                info["role"] = "NWP/Reanalysis In-Situ Verification / Boundary Feature"
                
            elif "circulation" in filename:
                df = pd.read_csv(filepath)
                info["num_records"] = len(df)
                info["columns"] = list(df.columns)
                info["missing_count"] = int(df.isna().sum().sum())
                info["duplicates"] = int(df.duplicated().sum())
                info["frequency"] = "Sub-daily / daily"
                info["variables"] = ", ".join(list(df.columns))
                info["role"] = "Atmospheric Circulation / Pressure Feature"
                
            elif filename.startswith("sm_"):
                # Soil moisture state files
                df = pd.read_csv(filepath)
                info["num_records"] = len(df)
                info["columns"] = list(df.columns)
                info["missing_count"] = int(df.isna().sum().sum())
                info["duplicates"] = int(df.duplicated().sum())
                state_name = filename.replace("sm_", "").replace("_2020.csv", "")
                info["spatial_coverage"] = f"State: {state_name} (District-level)"
                info["time_min"] = "2020-01-01 (Estimated)"
                info["time_max"] = "2020-12-31"
                info["frequency"] = "Daily / Weekly"
                info["variables"] = ", ".join(list(df.columns))
                info["units"] = "Soil Moisture Index / m³/m³"
                info["role"] = "Land Surface / Soil Moisture Feature (2020 only)"
                
        elif ext == ".tiff" or ext == ".tif":
            with tifffile.TiffFile(filepath) as tif:
                shape = tif.pages[0].shape
                dtype = tif.pages[0].dtype
                tags = {tag.name: tag.value for tag in tif.pages[0].tags}
                
                # Read sample or stats
                data = tif.pages[0].asarray()
                nodata = tags.get("GDAL_NODATA", -9999.0)
                valid_mask = (data > -1000) & (data < 10000)
                valid_data = data[valid_mask]
                
                info["raster_dimensions"] = shape
                info["pixel_dtype"] = str(dtype)
                info["nodata_value"] = str(nodata)
                info["elevation_min_m"] = float(valid_data.min()) if len(valid_data) else None
                info["elevation_max_m"] = float(valid_data.max()) if len(valid_data) else None
                info["elevation_mean_m"] = float(valid_data.mean()) if len(valid_data) else None
                info["spatial_coverage"] = "West Bengal Terrain DEM (SRTM / ASTER)"
                info["variables"] = "Surface Elevation"
                info["units"] = "meters above sea level"
                info["role"] = "Static Topographic Feature"
                
        elif ext == ".pdf":
            reader = pypdf.PdfReader(filepath)
            info["num_pages"] = len(reader.pages)
            extracted_text = ""
            for p in reader.pages[:3]:
                extracted_text += p.extract_text() or ""
            info["extracted_text_preview"] = extracted_text[:800].replace("\n", " ")
            if "DISTRICT_RAINFALL" in filename:
                info["role"] = "IMD Observed District Rainfall Distribution Report"
            elif "wind" in filename:
                info["role"] = "Wind Field Visualization / Reference"
                
        elif ext in [".png", ".jpg", ".webp"]:
            im = Image.open(filepath)
            info["image_dimensions"] = im.size
            info["image_mode"] = im.mode
            info["role"] = "Reference / Visual Validation Artifact"
            
    except Exception as e:
        info["status"] = f"ERROR: {str(e)}"
        
    return info

def main():
    files = sorted(glob.glob(os.path.join(RAW_DIR, "*")))
    results = []
    print(f"Auditing {len(files)} files in {RAW_DIR}...\n")
    for f in files:
        res = audit_file(f)
        results.append(res)
        print(f"Audit: {res['filename']} [{res['format']}] - Size: {res['size_bytes']:,} bytes - Role: {res.get('role', 'Unknown')}")
        
    output_path = "/Users/adityasingh/FINAL 086/data/raw_data_audit.json"
    with open(output_path, "w") as out_f:
        json.dump(results, out_f, indent=2)
    print(f"\nAudit complete. Detailed report saved to {output_path}")

if __name__ == "__main__":
    main()
