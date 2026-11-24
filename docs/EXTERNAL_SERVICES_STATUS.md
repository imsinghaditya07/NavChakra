# External Services & API Registration Status
**SIH 2026 Problem Statement 26086**

| Service / Source | URL / Provider | Tier / Status | Integration Strategy / Fallback |
|---|---|---|---|
| **ISRO MOSDAC** | `mosdac.gov.in` | **REGISTRATION SUBMITTED (Pending MoES/ISRO Approval)** | Utilizing verified INSAT-3D/3DR TIR1/TIR2 sample rasters and synthetic convective rapid-scan brightness temperature time series in `/data/sample/insat3d/`. Zero blockage to ML pipeline. |
| **Copernicus CDS (ERA5)** | `cds.climate.copernicus.eu` | **ACCOUNT CREATED (API Key Terms Pending)** | Using Open-Meteo Historical Reanalysis API (free, open, no key required) and IMD gridded daily data format for atmospheric instability, CAPE, and temperature profiles. |
| **IMD Gridded Rainfall** | `imdpune.gov.in` | Free open meteorological archive | Formatted 0.25° x 0.25° binary/NetCDF sample grids ingested into `/data/sample/imd_gridded/`. |
| **NOAA Climate Indices** | `psl.noaa.gov` | Free open public datasets | Automated HTTP fetchers for ONI (ENSO 3.4), BOM IOD Dipole Mode Index, and CPC MJO RMM1/RMM2 indices. |
| **Open-Meteo Live API** | `open-meteo.com` | 100% Free / Open (No API Key Required) | Direct real-time endpoint for hourly CAPE, surface pressure, soil moisture proxy, temperature, and wind gusts. |
| **NASA POWER API** | `power.larc.nasa.gov` | 100% Free / Open (No API Key Required) | REST API for agroclimatology features: All-Sky Surface Solar Irradiance, Root Zone Soil Wetness, and Dew Point. |
| **Blitzortung Lightning** | `blitzortung.org` | Free Community Network | Live and historical stroke density nowcast stream. |
| **Bhashini / IndicTrans2** | Bhashini Govt of India / AI4Bharat | Free Open Government Platform | Multi-lingual translation pipeline with Web Speech API browser-native fallback. |
| **DVC Version Control** | `dvc.org` | Configured and Initialized | Local and remote tracking for model weights and dataset splits. |
| **Hugging Face / Render** | `huggingface.co` / `render.com` | Free Tier (Container / Space) | Target host for Dockerized FastAPI inference and ONNX Runtime. |
