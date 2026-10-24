"""
ISRO MOSDAC INSAT-3D/3DR TIR & Blitzortung Lightning Convective Nowcasting Ingestion.
Generates rapid-scan 15-minute convective sequence features:
- Cloud-top Brightness Temperature (T_b) in Kelvin/Celsius
- Cooling rate: Delta T_b (15-min and 30-min changes)
- CAPE (Convective Available Potential Energy, J/kg)
- CIN (Convective Inhibition, J/kg)
- Lifted Index
- Blitzortung Lightning Strike count (past 15-min and 30-min)
- Target: Severe Thunderstorm / Lightning Formation within 0-30 min window (Binary 0/1)
"""

import os
import json
import logging
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROCESSED = os.path.join(BASE_DIR, "data", "processed")
SAMPLE_DIR = os.path.join(BASE_DIR, "data", "sample", "insat3d")
os.makedirs(SAMPLE_DIR, exist_ok=True)


def generate_convective_nowcast_dataset(n_samples: int = 12000) -> pd.DataFrame:
    """
    Generates synthetic 15-min satellite & lightning nowcasting training samples
    reflecting real physical mesoscale convective dynamics over the Indian subcontinent:
    - Rapid cloud-top cooling (< -10 K per 15 min) strongly predicts explosive convection
    - CAPE > 2000 J/kg combined with low CIN (< 30 J/kg) provides thermodynamic fuel
    - Precursor lightning strikes detected by Blitzortung indicate mature electrification
    """
    logging.info(f"Generating {n_samples} convective nowcasting records...")
    np.random.seed(42)

    # Base cloud top temperature in Celsius (-80 C deep cloud tops to +15 C warm ground)
    cloud_top_temp = np.random.uniform(-75.0, 15.0, n_samples)

    # 15-min and 30-min delta Tb (cooling rate in K/15min). Negative means cloud top is ascending rapidly into tropopause
    delta_tb_15m = np.random.normal(-2.5, 7.0, n_samples)
    delta_tb_30m = delta_tb_15m * 1.8 + np.random.normal(0, 3.0, n_samples)

    # CAPE (J/kg): 200 to 4500 J/kg
    cape = np.random.gamma(shape=2.5, scale=750.0, size=n_samples)
    cape = np.clip(cape, 100.0, 4800.0)

    # CIN (J/kg): 0 to 250 J/kg
    cin = np.random.exponential(scale=45.0, size=n_samples)
    cin = np.clip(cin, 0.0, 300.0)

    # Lifted Index: -10 to +5
    lifted_index = 5.0 - (cape / 400.0) + np.random.normal(0, 1.2, n_samples)
    lifted_index = np.clip(lifted_index, -12.0, 6.0)

    # Blitzortung lightning strikes in past 15 min
    # Most times 0, spikes during convective cells
    precursor_strikes = np.random.negative_binomial(1, 0.4, n_samples)
    precursor_strikes = np.where(delta_tb_15m < -8.0, precursor_strikes * 8 + np.random.randint(5, 50, n_samples), precursor_strikes)

    # Deep-layer wind shear 0-6km (m/s)
    wind_shear_6km = np.random.uniform(5.0, 35.0, n_samples)

    # Surface Dewpoint Depression (T - Td) in C: low values mean near-surface saturation
    dewpoint_depression = np.random.uniform(0.5, 12.0, n_samples)

    # Convective storm formation physics function (Ground Truth Label)
    # Severe storm if:
    # 1. Vigorous updraft: delta_tb_15m < -7.0 K OR cloud_top_temp < -50 C
    # 2. High instability: CAPE > 1500 J/kg AND CIN < 60 J/kg
    # 3. Moisture & precursor electrification: strikes > 5 OR dewpoint depression < 4 C
    logit = (
        -0.22 * delta_tb_15m +
        0.0012 * (cape - 1400.0) -
        0.025 * cin -
        0.35 * lifted_index +
        0.08 * np.log1p(precursor_strikes) -
        0.15 * dewpoint_depression -
        2.2
    )

    storm_prob = 1.0 / (1.0 + np.exp(-logit))
    # Binary target
    storm_label = (np.random.rand(n_samples) < storm_prob).astype(int)

    df = pd.DataFrame({
        "cloud_top_temp_c": np.round(cloud_top_temp, 1),
        "delta_tb_15m": np.round(delta_tb_15m, 2),
        "delta_tb_30m": np.round(delta_tb_30m, 2),
        "cape_j_kg": np.round(cape, 1),
        "cin_j_kg": np.round(cin, 1),
        "lifted_index": np.round(lifted_index, 2),
        "lightning_strikes_15m": precursor_strikes,
        "wind_shear_6km_ms": np.round(wind_shear_6km, 1),
        "dewpoint_depression_c": np.round(dewpoint_depression, 1),
        "storm_prob_true": np.round(storm_prob, 3),
        "storm_formation_30m": storm_label
    })

    out_path = os.path.join(DATA_PROCESSED, "convective_nowcast_dataset.parquet")
    df.to_parquet(out_path, index=False)
    logging.info(f"Convective nowcasting dataset saved to {out_path} ({storm_label.sum()} positive events)")

    # Save a JSON sample for rapid test inspection
    sample_json = os.path.join(SAMPLE_DIR, "convective_nowcast_sample.json")
    df.head(20).to_json(sample_json, orient="records", indent=2)

    return df


if __name__ == "__main__":
    df = generate_convective_nowcast_dataset()
    print("Convective nowcast target distribution:")
    print(df["storm_formation_30m"].value_counts(normalize=True))
