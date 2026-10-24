"""
Model B: Convective Nowcasting (0-30 Min Severe Thunderstorm & Lightning Formation)
Training Pipeline: LightGBM Convective Classifier + ONNX Export
Inputs: INSAT-3D TIR delta Tb, CAPE, CIN, Lifted Index, Blitzortung Strikes, Wind Shear
Output: Severe Thunderstorm Probability (0-100%) refreshed every 10-15 minutes
"""

import os
import json
import logging
import joblib
import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, brier_score_loss, accuracy_score, f1_score, precision_score, recall_score
import onnx
import onnxruntime as ort

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_FILE = os.path.join(BASE_DIR, "data", "processed", "convective_nowcast_dataset.parquet")
MODELS_DIR = os.path.join(BASE_DIR, "models", "saved")
EVAL_DIR = os.path.join(BASE_DIR, "models", "eval")

NOWCAST_FEATURES = [
    "cloud_top_temp_c",
    "delta_tb_15m",
    "delta_tb_30m",
    "cape_j_kg",
    "cin_j_kg",
    "lifted_index",
    "lightning_strikes_15m",
    "wind_shear_6km_ms",
    "dewpoint_depression_c"
]

TARGET_COL = "storm_formation_30m"


def train_model_b_nowcast():
    logging.info(f"Loading Convective Nowcast dataset from {DATA_FILE}...")
    df = pd.read_parquet(DATA_FILE)

    X = df[NOWCAST_FEATURES]
    y = df[TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    logging.info(f"Train samples: {len(X_train)} | Test samples: {len(X_test)}")

    params = {
        "objective": "binary",
        "metric": "binary_logloss",
        "boosting_type": "gbdt",
        "learning_rate": 0.05,
        "num_leaves": 25,
        "max_depth": 5,
        "feature_fraction": 0.9,
        "bagging_fraction": 0.85,
        "bagging_freq": 3,
        "verbose": -1,
        "random_state": 42
    }

    train_data = lgb.Dataset(X_train, label=y_train)
    val_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

    gbm = lgb.train(
        params,
        train_data,
        num_boost_round=120,
        valid_sets=[train_data, val_data],
        callbacks=[lgb.early_stopping(stopping_rounds=15, verbose=False)]
    )

    # Test set predictions
    y_prob = gbm.predict(X_test, num_iteration=gbm.best_iteration)
    y_pred = (y_prob >= 0.5).astype(int)

    auc = roc_auc_score(y_test, y_prob)
    brier = brier_score_loss(y_test, y_prob)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    logging.info(f"Model B Test AUC: {auc:.4f} | Brier Score: {brier:.4f} | Accuracy: {acc*100:.2f}% | Recall: {rec*100:.2f}%")

    # Feature Importance for Explainability
    importances = gbm.feature_importance(importance_type="gain")
    feat_imp = {feat: round(float(imp), 2) for feat, imp in zip(NOWCAST_FEATURES, importances)}
    # Sort descending
    feat_imp_sorted = dict(sorted(feat_imp.items(), key=lambda item: item[1], reverse=True))

    report = {
        "model_name": "Model B Convective Nowcast (0-30 min)",
        "test_metrics": {
            "roc_auc": round(float(auc), 4),
            "brier_score": round(float(brier), 4),
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4)
        },
        "feature_importance_gain": feat_imp_sorted
    }

    with open(os.path.join(EVAL_DIR, "model_b_evaluation_report.json"), "w") as f:
        json.dump(report, f, indent=2)

    # Save model weights
    joblib.dump(gbm, os.path.join(MODELS_DIR, "model_b_nowcast.pkl"))
    gbm.save_model(os.path.join(MODELS_DIR, "model_b_nowcast.txt"))

    # Export to ONNX for ultra-low latency CPU serving (<10ms)
    logging.info("Exporting Model B to ONNX format...")
    try:
        from onnxmltools import convert_lightgbm
        from onnxmltools.convert.common.data_types import FloatTensorType
        initial_types = [("float_input", FloatTensorType([None, len(NOWCAST_FEATURES)]))]
        onnx_model = convert_lightgbm(gbm, initial_types=initial_types, target_opset=12)
        onnx_path = os.path.join(MODELS_DIR, "model_b_nowcast.onnx")
        onnx.save_model(onnx_model, onnx_path)
        logging.info(f"Model B successfully exported to ONNX: {onnx_path}")
    except Exception as e:
        logging.warning(f"ONNX tools export note: {e}. Saved primary LightGBM runtime model.")

    return gbm, report


if __name__ == "__main__":
    train_model_b_nowcast()
