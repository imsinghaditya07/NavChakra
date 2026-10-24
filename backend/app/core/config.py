"""
Application Configuration and Environment Settings.
SIH 2026 Problem Statement 26086 - 100% Free / Open Tier Architecture.
"""

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Hyperlocal Monsoon Onset & Break Prediction System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "moes-ncmrwf-sih2026-hyperlocal-key-991283")
    OFFICIALS_USER: str = os.getenv("OFFICIALS_USER", "officials")
    OFFICIALS_PASSWORD: str = os.getenv("OFFICIALS_PASSWORD", "sih2026disaster")
    
    # Free Hosting / Cold-Start notes
    HOSTING_TIER: str = "Free Tier (Hugging Face Spaces / Render / Localhost)"
    COLD_START_NOTE: str = "Free tier instances may experience a 30s cold-start on inactivity. Auto-wake ping recommended."
    
    # Rate Limiting (SlowAPI)
    DEFAULT_RATE_LIMIT: str = "60/minute"
    PREDICT_RATE_LIMIT: str = "30/minute"
    
    # Free External Endpoints
    OPEN_METEO_URL: str = "https://api.open-meteo.com/v1/forecast"
    RAINVIEWER_RADAR_URL: str = "https://api.rainviewer.com/public/weather-maps.json"
    BLITZORTUNG_URL: str = "https://data.blitzortung.org/Data/Protected/live.json"
    BHASHINI_ENDPOINT: str = "https://nmt-models.bhashini.gov.in/v1/translate"
    HF_INFERENCE_API: str = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
    
    # Agent37 Agentic Layer Configuration
    AGENT37_API_KEY: str = os.getenv("AGENT37_API_KEY", "")
    AGENT37_API_BASE: str = os.getenv("AGENT37_API_BASE", "https://api.agent37.com")
    AGENT37_INSTANCE_ID: str = os.getenv("AGENT37_INSTANCE_ID", "")
    AGENT37_INSTANCE_URL: str = os.getenv("AGENT37_INSTANCE_URL", "")
    AGENT37_TIMEOUT_S: float = float(os.getenv("AGENT37_TIMEOUT_S", "8.0"))
    AGENT_TOOLS_KEY: str = os.getenv("AGENT_TOOLS_KEY", "")

    # Privacy Statement
    PRIVACY_CONSENT_NOTICE: str = "Farmer location and phone data are stored solely for automated agromet advisory delivery under MoES guidelines and are strictly never shared, monetized, or sold."

    model_config = {"case_sensitive": True, "extra": "ignore"}

settings = Settings()
