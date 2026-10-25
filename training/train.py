#!/usr/bin/env python3
"""
NavChakra ML Training Pipeline
Trains Tabular (LightGBM/XGBoost) and Temporal Sequence (PyTorch LSTM) models
for hyperlocal monsoon onset and break prediction.

CLI:
    python training/train.py --data data/sample/rainfall_sample.csv --out models/registry/v_sample --epochs 10
"""

import os
import sys
import json
import time
import argparse
import logging
from datetime import datetime
from typing import Dict, Any, Tuple, List

import numpy as np
import pandas as pd
import joblib

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

FEATURE_COLS = [
    "elevation_m",
    "day_of_year",
    "temp_max_c",
    "temp_min_c",
    "solar_radiation_mj",
    "rain_mm",
    "rain_7d_sum",
    "rain_14d_sum",
    "soil_wetness_rootzone",
    "enso_oni",
    "iod_dmi"
]

TARGET_COL = "monsoon_state"
CLASS_NAMES = ["Normal/Transition", "Onset Phase", "Active Monsoon", "Break Monsoon"]


# ==============================================================================
# PyTorch LSTM Sequence Model Architecture
# ==============================================================================

class MonsoonLSTM(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int = 64, num_layers: int = 2, num_classes: int = 4, dropout: float = 0.2):
        super(MonsoonLSTM, self).__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.num_classes = num_classes
        
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0
        )
        self.fc = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        # x shape: [batch_size, seq_len, input_dim]
        lstm_out, _ = self.lstm(x)
        # Use final sequence step representation
        last_step = lstm_out[:, -1, :]
        logits = self.fc(last_step)
        return logits


class SlidingWindowDataset(Dataset):
    def __init__(self, X: np.ndarray, y: np.ndarray, seq_len: int = 7):
        self.X_seqs = []
        self.y_labels = []
        for i in range(len(X) - seq_len + 1):
            self.X_seqs.append(X[i : i + seq_len])
            self.y_labels.append(y[i + seq_len - 1])

        if len(self.X_seqs) == 0:
            # Fallback for very small sequences
            self.X_seqs = [np.repeat(X[:1], seq_len, axis=0)]
            self.y_labels = [y[0] if len(y) > 0 else 0]

        self.X_seqs = torch.tensor(np.array(self.X_seqs), dtype=torch.float32)
        self.y_labels = torch.tensor(np.array(self.y_labels), dtype=torch.long)

    def __len__(self):
        return len(self.y_labels)

    def __getitem__(self, idx):
        return self.X_seqs[idx], self.y_labels[idx]


# ==============================================================================
# Training Logic
# ==============================================================================

def train_tabular_model(X_train: pd.DataFrame, y_train: pd.Series, X_val: pd.DataFrame, y_val: pd.Series) -> Tuple[Any, Dict[str, float]]:
    """Trains a LightGBM or XGBoost multi-class classifier."""
    logging.info("Training Tabular Model (LightGBM/XGBoost)...")
    try:
        import lightgbm as lgb
        model = lgb.LGBMClassifier(
            objective="multiclass",
            num_class=len(CLASS_NAMES),
            n_estimators=100,
            learning_rate=0.05,
            max_depth=5,
            random_state=42,
            verbosity=-1
        )
        model.fit(X_train, y_train)
    except ImportError:
        try:
            import xgboost as xgb
            model = xgb.XGBClassifier(
                objective="multi:softmax",
                num_class=len(CLASS_NAMES),
                n_estimators=100,
                learning_rate=0.05,
                max_depth=5,
                random_state=42
            )
            model.fit(X_train, y_train)
        except ImportError:
            from sklearn.ensemble import RandomForestClassifier
            model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
            model.fit(X_train, y_train)

    from sklearn.metrics import accuracy_score, f1_score
    preds = model.predict(X_val)
    acc = float(accuracy_score(y_val, preds))
    f1 = float(f1_score(y_val, preds, average="macro", zero_division=0))

    metrics = {
        "tabular_accuracy": round(acc, 4),
        "tabular_f1_macro": round(f1, 4)
    }
    logging.info(f"Tabular Model validation - Accuracy: {acc:.4f}, F1-Macro: {f1:.4f}")
    return model, metrics


def train_lstm_model(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: np.ndarray,
    y_val: np.ndarray,
    out_dir: str,
    epochs: int = 10,
    batch_size: int = 32,
    checkpoint_interval: int = 2,
    resume: bool = True
) -> Tuple[MonsoonLSTM, Dict[str, float]]:
    """Trains PyTorch LSTM with auto-checkpointing and resumable execution."""
    seq_len = 7
    train_ds = SlidingWindowDataset(X_train, y_train, seq_len=seq_len)
    val_ds = SlidingWindowDataset(X_val, y_val, seq_len=seq_len)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logging.info(f"Training LSTM Model on compute device: {device}")

    model = MonsoonLSTM(input_dim=X_train.shape[1], hidden_dim=64, num_layers=2, num_classes=len(CLASS_NAMES))
    model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.003, weight_decay=1e-4)

    start_epoch = 1
    checkpoint_latest_path = os.path.join(out_dir, "checkpoint_latest.pt")

    if resume and os.path.exists(checkpoint_latest_path):
        logging.info(f"Resuming training from latest checkpoint: {checkpoint_latest_path}")
        ckpt = torch.load(checkpoint_latest_path, map_location=device)
        model.load_state_dict(ckpt["model_state_dict"])
        optimizer.load_state_dict(ckpt["optimizer_state_dict"])
        start_epoch = ckpt["epoch"] + 1
        logging.info(f"Resumed successfully at Epoch {start_epoch}/{epochs}")

    for epoch in range(start_epoch, epochs + 1):
        model.train()
        total_loss = 0.0
        for batch_x, batch_y in train_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            optimizer.zero_grad()
            logits = model(batch_x)
            loss = criterion(logits, batch_y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        avg_loss = total_loss / max(1, len(train_loader))
        if epoch % max(1, checkpoint_interval) == 0 or epoch == epochs:
            logging.info(f"Epoch [{epoch}/{epochs}] - Loss: {avg_loss:.4f}")
            # Save checkpoint
            checkpoint_data = {
                "epoch": epoch,
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "loss": avg_loss
            }
            torch.save(checkpoint_data, checkpoint_latest_path)
            torch.save(checkpoint_data, os.path.join(out_dir, f"checkpoint_epoch_{epoch}.pt"))

    # Evaluation on Validation Set
    model.eval()
    correct = 0
    total = 0
    all_preds, all_targets = [], []

    with torch.no_grad():
        for batch_x, batch_y in val_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            logits = model(batch_x)
            preds = torch.argmax(logits, dim=1)
            correct += (preds == batch_y).sum().item()
            total += batch_y.size(0)
            all_preds.extend(preds.cpu().numpy().tolist())
            all_targets.extend(batch_y.cpu().numpy().tolist())

    from sklearn.metrics import accuracy_score, f1_score
    acc = float(accuracy_score(all_targets, all_preds)) if total > 0 else 0.0
    f1 = float(f1_score(all_targets, all_preds, average="macro", zero_division=0)) if total > 0 else 0.0

    metrics = {
        "lstm_accuracy": round(acc, 4),
        "lstm_f1_macro": round(f1, 4)
    }
    logging.info(f"LSTM Model validation - Accuracy: {acc:.4f}, F1-Macro: {f1:.4f}")
    return model, metrics


def main():
    parser = argparse.ArgumentParser(description="NavChakra Model Training Engine")
    parser.add_argument("--data", type=str, required=True, help="Path to input training CSV or Parquet")
    parser.add_argument("--out", type=str, required=True, help="Directory to save artifacts and checkpoints")
    parser.add_argument("--epochs", type=int, default=10, help="Number of LSTM training epochs")
    parser.add_argument("--checkpoint-interval", type=int, default=2, help="Checkpoint interval in epochs")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size")
    parser.add_argument("--no-resume", action="store_true", help="Disable resuming from checkpoint")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)
    version_tag = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    logging.info(f"Starting Training Job. Version tag: {version_tag}")
    logging.info(f"Loading data from: {args.data}")

    if args.data.endswith(".parquet"):
        df = pd.read_parquet(args.data)
    else:
        df = pd.read_csv(args.data)

    # Validate required columns
    available_features = [col for col in FEATURE_COLS if col in df.columns]
    if len(available_features) < 3:
        raise ValueError(f"Insufficient features in input data. Available: {list(df.columns)}")

    if TARGET_COL not in df.columns:
        # Fallback target column check
        if "monsoon_state_id" in df.columns:
            df[TARGET_COL] = df["monsoon_state_id"]
        else:
            raise ValueError(f"Target column '{TARGET_COL}' not found in data.")

    # Sort by date for temporal consistency
    if "date" in df.columns:
        df = df.sort_values("date").reset_index(drop=True)

    split_idx = int(len(df) * 0.8)
    train_df = df.iloc[:split_idx]
    val_df = df.iloc[split_idx:]

    X_train = train_df[available_features]
    y_train = train_df[TARGET_COL].astype(int)
    X_val = val_df[available_features]
    y_val = val_df[TARGET_COL].astype(int)

    logging.info(f"Train split: {len(X_train)} samples | Val split: {len(X_val)} samples")

    # 1. Train Tabular Model
    tab_model, tab_metrics = train_tabular_model(X_train, y_train, X_val, y_val)
    tab_model_path = os.path.join(args.out, "model_tabular.pkl")
    joblib.dump({"model": tab_model, "features": available_features, "classes": CLASS_NAMES}, tab_model_path)
    logging.info(f"Saved tabular model -> {tab_model_path}")

    # 2. Train LSTM Model
    # Normalize features for neural network
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_train_norm = scaler.fit_transform(X_train.fillna(0))
    X_val_norm = scaler.transform(X_val.fillna(0))

    lstm_model, lstm_metrics = train_lstm_model(
        X_train_norm,
        y_train.values,
        X_val_norm,
        y_val.values,
        out_dir=args.out,
        epochs=args.epochs,
        batch_size=args.batch_size,
        checkpoint_interval=args.checkpoint_interval,
        resume=(not args.no_resume)
    )
    lstm_model_path = os.path.join(args.out, "model_lstm.pt")
    torch.save({
        "state_dict": lstm_model.state_dict(),
        "input_dim": len(available_features),
        "hidden_dim": 64,
        "num_layers": 2,
        "num_classes": len(CLASS_NAMES),
        "scaler": scaler,
        "features": available_features
    }, lstm_model_path)
    logging.info(f"Saved LSTM model -> {lstm_model_path}")

    # 3. Save Metrics & Metadata
    all_metrics = {
        **tab_metrics,
        **lstm_metrics,
        "train_samples": len(X_train),
        "val_samples": len(X_val),
        "evaluated_at": datetime.utcnow().isoformat() + "Z"
    }
    metrics_path = os.path.join(args.out, "metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(all_metrics, f, indent=2)

    metadata = {
        "version": version_tag,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "features": available_features,
        "classes": CLASS_NAMES,
        "metrics": all_metrics,
        "artifacts": {
            "tabular": "model_tabular.pkl",
            "lstm": "model_lstm.pt",
            "metrics": "metrics.json"
        }
    }
    metadata_path = os.path.join(args.out, "metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    logging.info(f"Training completed successfully! Metrics saved to {metrics_path}")
    print(json.dumps({"status": "success", "version": version_tag, "metrics": all_metrics}))

if __name__ == "__main__":
    main()
