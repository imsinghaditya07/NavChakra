# Multi-stage Dockerfile for Hugging Face Spaces / Render Free Tier
# SIH 2026 Problem Statement 26086 - Hyperlocal Monsoon Prediction System
FROM python:3.9-slim

# Prevent Python from writing .pyc and buffer stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=7860

WORKDIR /app

# Install system dependencies including OpenMP for LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY data/ ./data/
COPY models/ ./models/
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY docs/ ./docs/

# Seed DB and test models on container build
RUN python -c "from backend.app.db.database import init_db; init_db()"

EXPOSE 7860

# Run FastAPI server via Uvicorn
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "7860"]
