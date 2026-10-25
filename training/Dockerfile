# ==============================================================================
# NavChakra GPU Training Container
# Designed for external GPU compute providers (Nodus, RunPod, Lambda, etc.)
# ==============================================================================

FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    CUDA_VISIBLE_DEVICES=0

# System build dependencies for LightGBM and scientific compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Install training dependencies
COPY requirements.txt /workspace/
RUN pip install --no-cache-dir -r requirements.txt

# Copy training pipeline and data generation utilities
COPY __init__.py generate_sample_data.py train.py runner.py storage.py /workspace/training/

# Default entrypoint runs training CLI
ENTRYPOINT ["python", "training/train.py"]
CMD ["--data", "/data/rainfall.csv", "--out", "/models/artifacts", "--epochs", "20"]
