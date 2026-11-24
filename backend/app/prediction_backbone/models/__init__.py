"""Models package."""
from backend.app.prediction_backbone.models.weather_event_model import weather_event_model
from backend.app.prediction_backbone.models.parameter_models import parameter_models

__all__ = ["weather_event_model", "parameter_models"]
