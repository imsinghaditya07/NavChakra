#!/usr/bin/env python3
"""
Generate synthetic block-level historical rainfall and agromet observations.
Used for end-to-end pipeline validation and testing of the NavChakra ML system.
"""

import os
import argparse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

SAMPLE_BLOCKS = [
    {"block_id": "MH_YVT_01", "name": "Yavatmal", "elevation_m": 445.0, "base_rain": 2.8},
    {"block_id": "WB_BIR_01", "name": "Bolpur Sriniketan", "elevation_m": 58.0, "base_rain": 3.6},
    {"block_id": "KA_BLR_01", "name": "Anekal", "elevation_m": 915.0, "base_rain": 2.4},
    {"block_id": "UP_VAR_01", "name": "Pindra", "elevation_m": 82.0, "base_rain": 3.1},
    {"block_id": "KL_WYD_01", "name": "Vythiri", "elevation_m": 1200.0, "base_rain": 7.5},
]

MONSOON_CLASSES = {
    0: "Normal/Transition",
    1: "Onset Phase",
    2: "Active Monsoon",
    3: "Break Monsoon"
}

def generate_sample_dataset(output_path: str, days: int = 730, seed: int = 42) -> str:
    """
    Generates realistic synthetic multi-block timeseries data for monsoon prediction.
    """
    np.random.seed(seed)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    start_date = datetime(2024, 1, 1)
    rows = []

    for block in SAMPLE_BLOCKS:
        b_id = block["block_id"]
        elev = block["elevation_m"]
        base_r = block["base_rain"]
        
        # Cumulative rolling memory
        recent_rain = []

        for d in range(days):
            current_date = start_date + timedelta(days=d)
            doy = current_date.timetuple().tm_yday
            
            # Seasonal monsoon modulation: peak in June-September (doy 150-270)
            is_monsoon_season = 150 <= doy <= 270
            monsoon_intensity = np.sin((doy - 150) / 120 * np.pi) if is_monsoon_season else 0.0
            monsoon_intensity = max(0.0, monsoon_intensity)

            # Atmospheric indices with slow drift
            enso_oni = round(float(np.sin(d / 120.0) * 1.2 + np.random.normal(0, 0.1)), 3)
            iod_dmi = round(float(np.cos(d / 90.0) * 0.6 + np.random.normal(0, 0.05)), 3)
            solar_rad = round(float(18.0 - (monsoon_intensity * 7.0) + np.random.normal(0, 1.5)), 2)
            temp_max = round(float(34.0 - (monsoon_intensity * 6.0) + np.random.normal(0, 2.0)), 1)
            temp_min = round(float(temp_max - 8.0 + np.random.normal(0, 1.0)), 1)

            # Daily rainfall generation
            if is_monsoon_season:
                # Stochastic active vs break cycle
                is_break = (np.sin(d / 14.0) < -0.4)
                if is_break:
                    rain_mm = round(float(np.random.exponential(1.5)), 1)
                else:
                    rain_mm = round(float(base_r * 4.5 * (1.0 + monsoon_intensity) + np.random.exponential(12.0)), 1)
            else:
                rain_mm = round(float(np.random.exponential(0.8) if np.random.rand() > 0.8 else 0.0), 1)

            recent_rain.append(rain_mm)
            rain_7d = sum(recent_rain[-7:])
            rain_14d = sum(recent_rain[-14:])
            soil_wetness = round(min(1.0, max(0.05, 0.15 + (rain_14d / 180.0) + np.random.normal(0, 0.03))), 3)

            # Label assignment based on physical dynamics
            if not is_monsoon_season:
                monsoon_state = 0  # Normal/Transition
            elif doy < 175 and rain_7d > 25.0:
                monsoon_state = 1  # Onset Phase
            elif rain_7d < 10.0:
                monsoon_state = 3  # Break Monsoon
            else:
                monsoon_state = 2  # Active Monsoon

            rows.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "block_id": b_id,
                "elevation_m": elev,
                "day_of_year": doy,
                "temp_max_c": temp_max,
                "temp_min_c": temp_min,
                "solar_radiation_mj": solar_rad,
                "rain_mm": rain_mm,
                "rain_7d_sum": round(rain_7d, 1),
                "rain_14d_sum": round(rain_14d, 1),
                "soil_wetness_rootzone": soil_wetness,
                "enso_oni": enso_oni,
                "iod_dmi": iod_dmi,
                "monsoon_state": monsoon_state
            })

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} synthetic weather records -> {output_path}")
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic block rainfall dataset for training")
    parser.add_argument("--output", type=str, default="data/sample/rainfall_sample.csv", help="Output CSV path")
    parser.add_argument("--days", type=int, default=730, help="Number of historical days per block")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    generate_sample_dataset(args.output, args.days, args.seed)
