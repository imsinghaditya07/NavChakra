"""
Export Model A (LightGBM) to ONNX for sub-millisecond CPU inference in FastAPI.
"""

import os
import joblib
import onnx
from onnxmltools import convert_lightgbm
from onnxmltools.convert.common.data_types import FloatTensorType

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODELS_DIR = os.path.join(BASE_DIR, "models", "saved")

def export_model_a():
    model_path = os.path.join(MODELS_DIR, "model_a_lightgbm.pkl")
    onnx_path = os.path.join(MODELS_DIR, "model_a_lightgbm.onnx")

    gbm = joblib.load(model_path)
    initial_types = [("float_input", FloatTensorType([None, 18]))]
    onnx_model = convert_lightgbm(gbm, initial_types=initial_types, target_opset=12)
    onnx.save_model(onnx_model, onnx_path)
    print(f"Model A successfully exported to ONNX: {onnx_path}")

if __name__ == "__main__":
    export_model_a()
