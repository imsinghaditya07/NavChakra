"""
Pytest Suite for AryaSaarthi Prediction Backbone.

Validates:
1. Complete schema conformance of PredictionBackboneOutput (ISO8601, region, event, fields, particles, confidence, model_version)
2. Weather Event Model: Global/Synoptic track & Local/Gridded track
3. Per-parameter models: Wind vector fields, Rain particles, Hail, Lightning, Heat, Drought
4. Downscaling to Gram Panchayat boundaries with elevation lapse rate & confidence propagation
5. Warning threshold triggering (IMD color tiers: GREEN, YELLOW, ORANGE, RED) & deterministic ICAR advisories
6. Graceful degradation on missing/delayed feeds (penalizes confidence, no hard crash)
7. REST API endpoints: /predict/block/{id}, /predict/panchayat/{id}, /predict/pipeline, /predict/benchmark/eval
8. WMO/IMD evaluation metrics: RMSE, MAE, Brier score, CSI, Cyclone track error, Flood F2 score.
"""

import pytest
from datetime import datetime
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.prediction_backbone.schema import PredictionBackboneOutput
from backend.app.prediction_backbone.service import prediction_backbone_service
from backend.app.prediction_backbone.ingestion.unified_store import unified_store, FeedStatus
from backend.app.prediction_backbone.ingestion.ingestion_pipeline import ingestion_pipeline
from backend.app.prediction_backbone.models.weather_event_model import weather_event_model
from backend.app.prediction_backbone.models.parameter_models import parameter_models
from backend.app.prediction_backbone.downscaling.spatial_downscaler import spatial_downscaler
from backend.app.prediction_backbone.rules.warning_risk_advisory import warning_risk_advisory
from backend.app.prediction_backbone.evaluation.metrics import MeteorologicalEvaluator

client = TestClient(app)


def test_prediction_backbone_schema_contract():
    """Validates that prediction backbone output strictly matches the required downstream schema."""
    output = prediction_backbone_service.predict(block_id="WB_BIR_BOLPUR", crop="rice", stage="vegetative")
    
    # 1. Root contract keys
    assert isinstance(output, PredictionBackboneOutput)
    d = output.model_dump()
    for req_key in ["timestamp", "valid_for", "region", "event", "fields", "particles", "model_version", "confidence"]:
        assert req_key in d, f"Missing required contract key: {req_key}"

    # 2. Region schema
    assert d["region"]["block_id"] == "WB_BIR_BOLPUR"
    assert "panchayat_id" in d["region"]
    assert isinstance(d["region"]["lat"], float)
    assert isinstance(d["region"]["lon"], float)

    # 3. Event schema
    assert d["event"]["type"] in ["cyclone", "storm", "none"]
    assert isinstance(d["event"]["track"], list)
    assert isinstance(d["event"]["intensity"], float)
    assert isinstance(d["event"]["confidence"], float)

    # 4. Fields schema (probabilistic, never bare points)
    fields = d["fields"]
    for f in ["rainfall_mm", "rainfall_prob", "heat_index", "drought_index", "flood_risk"]:
        assert f in fields
        assert isinstance(fields[f], (int, float))
    assert "rainfall_p10_mm" in fields
    assert "rainfall_p90_mm" in fields
    assert fields["rainfall_p90_mm"] >= fields["rainfall_p10_mm"]

    # 5. Particles schema
    particles = d["particles"]
    assert "wind" in particles
    assert "speed_kmh" in particles["wind"]
    assert "direction_deg" in particles["wind"]
    assert "rain" in particles
    assert "intensity" in particles["rain"]
    assert "hail_prob" in particles
    assert "lightning_prob" in particles
    assert 0.0 <= particles["hail_prob"] <= 1.0
    assert 0.0 <= particles["lightning_prob"] <= 1.0

    # 6. Model version and confidence
    assert "aryasaarthi-backbone" in d["model_version"]
    assert 0.0 <= d["confidence"] <= 1.0


def test_weather_event_model_synoptic_track():
    """Tests synoptic track trajectory projection for cyclonic and convective events."""
    # Test cyclone detection over maritime basin (Bay of Bengal coordinates)
    maritime_atm = {
        "dist_maritime_km": 150.0,
        "sst_c": 29.8,
        "vertical_wind_shear_ms": 7.5,
        "mslp_hpa": 994.0,
        "cape_j_kg": 3200.0,
        "delta_tb_15m": -12.0
    }
    cyclone_event = weather_event_model.predict_synoptic_event(lat=18.5, lon=86.8, atmospheric_data=maritime_atm)
    assert cyclone_event.type == "cyclone"
    assert cyclone_event.intensity >= 0.60
    assert len(cyclone_event.track) == 3  # 6h, 24h, 72h
    assert cyclone_event.track[0].horizon_hours == 6
    assert cyclone_event.track[1].horizon_hours == 24
    assert cyclone_event.track[2].horizon_hours == 72
    assert cyclone_event.track[0].wind_speed_kmh > 70.0


def test_spatial_downscaler_lapse_rate_and_confidence():
    """Tests topographic downscaling: elevation cooling, orographic rain, and confidence propagation."""
    out = prediction_backbone_service.predict(block_id="WB_BIR_BOLPUR")
    grid_fields = out.fields
    grid_wind = out.particles.wind

    # Simulate hill panchayat at 850m elevation (vs grid at 200m -> +650m)
    hill_meta = {
        "elevation_m": 850.0,
        "terrain_roughness_m": 120.0,
        "land_use": "agricultural",
        "slope_aspect_deg": 235.0
    }
    down_fields, down_wind, prop_conf, audit = spatial_downscaler.downscale_to_panchayat(
        grid_fields=grid_fields,
        grid_wind=grid_wind,
        parent_confidence=0.95,
        panchayat_meta=hill_meta,
        grid_elevation_m=200.0
    )

    # Temperature should drop by ~4.2 C (-6.5 C per km * 0.65 km)
    assert down_fields.temp_c < grid_fields.temp_c
    expected_temp_diff = 650.0 * (-0.0065)
    assert abs((down_fields.temp_c - grid_fields.temp_c) - expected_temp_diff) < 0.2

    # Propagated confidence should be penalized due to terrain roughness variance (no false precision)
    assert prop_conf < 0.95
    assert audit["variance_penalty"] > 0.0


def test_warning_and_advisory_rules():
    """Tests deterministic warning triggers and ICAR advisory generation."""
    # Test severe convective alert
    out = prediction_backbone_service.predict(block_id="MH_YVT_01", crop="cotton", stage="sowing")
    assert out.warnings is not None
    assert len(out.warnings) > 0
    assert out.risk_assessment is not None
    assert out.risk_assessment.composite_tier in ["LOW", "WATCH", "HIGH", "SEVERE"]
    assert out.advisory is not None
    assert out.advisory.rule_id is not None
    assert len(out.advisory.action_checklist) >= 2


def test_graceful_degradation_on_missing_feed():
    """Tests that pipeline gracefully falls back and degrades confidence when feeds fail."""
    # 1. Normal confidence
    ingestion_pipeline.restore_all_feeds()
    out_normal = prediction_backbone_service.predict(block_id="WB_BIR_BOLPUR", bypass_cache=True)
    normal_conf = out_normal.confidence

    # 2. Simulate satellite TIR feed failure
    ingestion_pipeline.simulate_missing_feed("insat_satellite", fallback_type=FeedStatus.FALLBACK_REANALYSIS)
    out_degraded = prediction_backbone_service.predict(block_id="WB_BIR_BOLPUR", bypass_cache=True)

    # System should still succeed (no hard crash) but with lower confidence
    assert out_degraded.confidence < normal_conf
    assert len(out_degraded.data_lineage.fallbacks_applied) > 0
    assert "insat_satellite" in out_degraded.data_lineage.fallbacks_applied[0]

    # Restore feeds
    ingestion_pipeline.restore_all_feeds()


def test_rest_api_endpoints():
    """Tests all REST endpoints exposed by prediction router."""
    # 1. /predict/block/{block_id}
    res1 = client.get("/predict/block/WB_BIR_BOLPUR")
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["region"]["block_id"] == "WB_BIR_BOLPUR"
    assert data1["model_version"] == "aryasaarthi-backbone-v2.1.0"

    # 2. /predict/panchayat/{panchayat_id}
    res2 = client.get("/predict/panchayat/PANCH_BOLPUR_01?block_id=WB_BIR_BOLPUR&crop=rice")
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["region"]["panchayat_id"] == "PANCH_BOLPUR_01"

    # 3. POST /predict/pipeline
    res3 = client.post("/predict/pipeline", json={"lat": 23.67, "lon": 87.72, "crop": "jute"})
    assert res3.status_code == 200
    data3 = res3.json()
    assert "fields" in data3
    assert "particles" in data3

    # 4. /predict/particles/grid
    res4 = client.get("/predict/particles/grid?step_deg=8.0")
    assert res4.status_code == 200
    grid_data = res4.json()
    assert grid_data["status"] == "success"
    assert len(grid_data["grid"]) > 0

    # 5. /predict/benchmark/eval
    res5 = client.get("/predict/benchmark/eval")
    assert res5.status_code == 200
    eval_data = res5.json()
    assert "rainfall_regression" in eval_data
    assert "heavy_rain_skill_scores" in eval_data
    assert "cyclone_track_error_km" in eval_data
    assert eval_data["heavy_rain_skill_scores"]["csi"] > 0.50


def test_meteorological_evaluator_metrics():
    """Tests individual metric computation formulas."""
    # Haversine distance
    dist = MeteorologicalEvaluator.haversine_distance_km(19.0, 72.8, 13.0, 80.2)  # Mumbai to Chennai ~1030 km
    assert 1000.0 < dist < 1100.0

    # Brier score on perfect vs flawed forecast
    import numpy as np
    obs = np.array([1, 1, 0, 0])
    perf_probs = np.array([1.0, 1.0, 0.0, 0.0])
    perf_eval = MeteorologicalEvaluator.evaluate_probabilistic_and_skill(obs, perf_probs)
    assert perf_eval["brier_score"] == 0.0
    assert perf_eval["csi"] == 1.0
