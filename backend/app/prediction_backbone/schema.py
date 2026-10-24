"""
Prediction Backbone Output Schema.
SIH 2026 / AryaSaarthi Prediction Engine Contract.

Every model in the prediction backbone emits a common, versioned schema consumed by
WeatherAnimationEngine, MapLibre/Leaflet rendering, the agromet advisory pipeline,
and administrative disaster management systems.
"""

from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict


class RegionSchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    block_id: str = Field(..., description="Unique Block/Tehsil identifier (e.g., WB_BIR_BOLPUR)")
    panchayat_id: str = Field(..., description="Unique Gram Panchayat identifier (e.g., PANCH_BOLPUR_01)")
    lat: float = Field(..., description="Latitude in decimal degrees")
    lon: float = Field(..., description="Longitude in decimal degrees")
    block_name: Optional[str] = Field(None, description="Human readable Block name")
    panchayat_name: Optional[str] = Field(None, description="Human readable Panchayat name")
    district: Optional[str] = Field(None, description="District name")
    state: Optional[str] = Field(None, description="State name")
    elevation_m: Optional[float] = Field(None, description="Elevation above sea level in meters")


class TrackPoint(BaseModel):
    model_config = ConfigDict(extra="allow")

    horizon_hours: int = Field(..., description="Forecast horizon in hours (e.g., 6, 24, 72)")
    valid_time: str = Field(..., description="ISO8601 validity timestamp for this waypoint")
    lat: float = Field(..., description="Waypoint latitude")
    lon: float = Field(..., description="Waypoint longitude")
    intensity: float = Field(..., description="Normalized system intensity [0.0 - 1.0]")
    wind_speed_kmh: float = Field(..., description="Maximum sustained wind speed in km/h")
    pressure_hpa: float = Field(..., description="Estimated central pressure in hPa")


class EventSchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    type: Literal["cyclone", "storm", "none"] = Field(..., description="System type: cyclone | storm | none")
    track: List[TrackPoint] = Field(default_factory=list, description="Projected trajectory waypoints (6h, 24h, 72h)")
    intensity: float = Field(..., description="Normalized system intensity [0.0 - 1.0]")
    confidence: float = Field(..., description="Model confidence score [0.0 - 1.0]")
    name: Optional[str] = Field(None, description="Official storm/cyclone name if named")
    category: Optional[str] = Field(None, description="IMD classification (e.g., 'Depression', 'Severe Cyclonic Storm')")


class FieldsSchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    rainfall_mm: float = Field(..., description="Expected 24-hour rainfall in millimeters (P50 median)")
    rainfall_prob: float = Field(..., description="Probability of measurable rainfall (>0.1 mm) [0.0 - 1.0]")
    heat_index: float = Field(..., description="Rothfusz/Steadman Heat Index in Celsius")
    drought_index: float = Field(..., description="Standardized Precipitation & Evapotranspiration Index (SPEI)")
    flood_risk: float = Field(..., description="Composite hydrological flood risk score [0.0 - 1.0]")
    
    # Extended probabilistic quantiles (never bare point estimates)
    rainfall_p10_mm: Optional[float] = Field(None, description="10th percentile rainfall (dry scenario)")
    rainfall_p90_mm: Optional[float] = Field(None, description="90th percentile rainfall (heavy rain scenario)")
    temp_c: Optional[float] = Field(None, description="Dry bulb surface temperature in Celsius")
    humidity_pct: Optional[float] = Field(None, description="Relative humidity percentage")
    soil_moisture_rootzone: Optional[float] = Field(None, description="Rootzone soil moisture fraction [0.0 - 1.0]")


class WindParticle(BaseModel):
    model_config = ConfigDict(extra="allow")

    speed_kmh: float = Field(..., description="Surface wind speed at 10m in km/h")
    direction_deg: float = Field(..., description="Wind direction in meteorological degrees (0-360, where 0=N, 90=E)")
    u_ms: Optional[float] = Field(None, description="Zonal wind vector component in m/s (eastward positive)")
    v_ms: Optional[float] = Field(None, description="Meridional wind vector component in m/s (northward positive)")


class RainParticle(BaseModel):
    model_config = ConfigDict(extra="allow")

    intensity: float = Field(..., description="Normalized rain particle render intensity [0.0 - 1.0]")
    density: Optional[float] = Field(None, description="Particle density for canvas/webgl particle renderer [0.0 - 1.0]")


class ParticlesSchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    wind: WindParticle = Field(..., description="Wind vector particle field")
    rain: RainParticle = Field(..., description="Rain intensity particle field")
    hail_prob: float = Field(..., description="Probability of hail occurrence [0.0 - 1.0]")
    lightning_prob: float = Field(..., description="Probability of lightning strike within 15-30 min [0.0 - 1.0]")


class WarningItem(BaseModel):
    code: str = Field(..., description="Warning identifier (e.g., 'HEAVY_RAIN_WARNING')")
    tier: Literal["GREEN", "YELLOW", "ORANGE", "RED"] = Field(..., description="IMD color-coded alert tier")
    title: str = Field(..., description="Short warning title")
    description: str = Field(..., description="Detailed meteorological alert context")
    threshold_triggered: str = Field(..., description="Explicit rule condition that fired")


class RiskAssessment(BaseModel):
    composite_tier: Literal["LOW", "WATCH", "HIGH", "SEVERE"] = Field(...)
    composite_score: float = Field(..., description="Normalized multi-hazard risk score [0.0 - 1.0]")
    crop_risk_tier: str = Field(...)
    flood_risk_tier: str = Field(...)
    drought_risk_tier: str = Field(...)
    storm_risk_tier: str = Field(...)


class AdvisoryItem(BaseModel):
    rule_id: str = Field(..., description="Deterministic ICAR/Agromet rule ID")
    urgency: Literal["LOW", "MODERATE", "HIGH", "IMMEDIATE"] = Field(...)
    crop: str = Field(...)
    stage: str = Field(...)
    advisory_en: str = Field(..., description="English agronomic advisory text")
    advisory_hi: str = Field(..., description="Hindi agronomic advisory text")
    advisory_local: Optional[str] = Field(None, description="Regional language advisory (Bengali, Marathi, etc.)")
    action_checklist: List[str] = Field(default_factory=list, description="Immediate actionable steps for farmer")


class DataLineage(BaseModel):
    feeds_ingested: List[str] = Field(default_factory=list)
    fallbacks_applied: List[str] = Field(default_factory=list)
    confidence_degraded_by: float = Field(0.0, description="Amount confidence was penalized due to missing feeds")


class PredictionBackboneOutput(BaseModel):
    """
    Unified Prediction Backbone Output Schema.
    Strictly conforms to required downstream schema:
    {
      "timestamp": ISO8601,
      "valid_for": ISO8601,
      "region": { "block_id", "panchayat_id", "lat", "lon" },
      "event": { "type", "track", "intensity", "confidence" },
      "fields": { "rainfall_mm", "rainfall_prob", "heat_index", "drought_index", "flood_risk" },
      "particles": { "wind", "rain", "hail_prob", "lightning_prob" },
      "model_version": string,
      "confidence": float
    }
    Plus optional enriched layers (warnings, risk_assessment, advisory, data_lineage).
    """
    model_config = ConfigDict(extra="allow")

    timestamp: str = Field(..., description="ISO8601 generation timestamp")
    valid_for: str = Field(..., description="ISO8601 forecast validity timestamp")
    region: RegionSchema = Field(..., description="Administrative and geospatial location")
    event: EventSchema = Field(..., description="Synoptic weather event tracking (cyclone/storm/none)")
    fields: FieldsSchema = Field(..., description="Continuous gridded meteorological fields")
    particles: ParticlesSchema = Field(..., description="Vector particle-level fields for animations")
    model_version: str = Field("aryasaarthi-backbone-v2.1.0", description="Semantic model version string")
    confidence: float = Field(..., description="Aggregated forecast confidence [0.0 - 1.0]")

    # Enriched operational extensions
    warnings: List[WarningItem] = Field(default_factory=list, description="Threshold-triggered color coded warnings")
    risk_assessment: Optional[RiskAssessment] = Field(None, description="Multi-hazard risk assessment")
    advisory: Optional[AdvisoryItem] = Field(None, description="Agronomic advisory based on risk and crop stage")
    data_lineage: Optional[DataLineage] = Field(None, description="Ingestion feeds, fallbacks, and audit trail")
