"""
Pytest Test Suite for SIH PS 26086 Hyperlocal Prediction Backend.
Validates:
- Model A Seasonal inference & XAI explanation
- Model B Convective nowcasting
- Deterministic Agronomic Advisory Rules (ICAR logic)
- Grounded RAG Chatbot (No hallucination)
- Emergency Crowd-Report Override Fallback
- Model Health & Drift Monitoring schema
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.services.advisory_engine import advisory_engine
from backend.app.services.rag_chatbot import rag_chatbot
from models.eval.fusion_engine import fusion_engine

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "Hyperlocal" in data["service"]


def test_get_blocks():
    response = client.get("/api/blocks")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["blocks"]) > 0
    assert "geojson" in data


def test_model_a_seasonal_prediction():
    response = client.get("/api/predict/seasonal/MH_YVT_01")
    assert response.status_code == 200
    data = response.json()
    assert "probabilities" in data
    assert "break_monsoon_pct" in data["probabilities"]
    assert "xai_explanation" in data
    assert "one_liner_en" in data["xai_explanation"]
    assert "one_liner_hi" in data["xai_explanation"]


def test_model_b_convective_nowcast():
    payload = {
        "cloud_top_temp_c": -55.0,
        "delta_tb_15m": -12.5,
        "delta_tb_30m": -22.0,
        "cape_j_kg": 2800.0,
        "cin_j_kg": 15.0,
        "lifted_index": -6.0,
        "lightning_strikes_15m": 25,
        "wind_shear_6km_ms": 22.0,
        "dewpoint_depression_c": 1.8
    }
    response = client.post("/api/predict/nowcast", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["storm_formation_probability_pct"] > 60.0
    assert data["lightning_hazard_level"] == "SEVERE_STORM_WARNING"
    assert "xai_attribution" in data


def test_advisory_rule_engine():
    # Test Rule 1: Break during sowing -> Delay sowing
    adv = advisory_engine.generate_advisory(crop="cotton", stage="sowing", prob_break=0.75, prob_storm=0.10)
    assert adv["rule_id"] == "RULE_SOW_BREAK_CRITICAL"
    assert adv["urgency"] == "HIGH"
    assert ("7-10" in adv["advisory_en"] or "7–10" in adv["advisory_en"])
    assert "पेरणी" in adv["advisory_mr"] or "बुवाई" in adv["advisory_hi"]

    # Test Rule 2: Convective storm alert -> Suspend field operations
    adv_storm = advisory_engine.generate_advisory(crop="paddy", stage="tillering", prob_break=0.10, prob_storm=0.85)
    assert adv_storm["rule_id"] == "RULE_STORM_NOWCAST_SEVERE"
    assert adv_storm["urgency"] == "IMMEDIATE"


def test_grounded_rag_chatbot():
    # Chatbot test about sowing during impending break
    block_ctx = {"block_name": "Pusad", "prob_break": 0.75, "prob_storm": 0.10, "soil_moisture": 0.25}
    res_en = rag_chatbot.answer_query("Should I sow cotton tomorrow?", block_context=block_ctx, lang="en")
    assert "Caution" in res_en["answer"] or "delay" in res_en["answer"].lower()
    assert res_en["grounding_status"] == "STRICTLY_GROUNDED_IN_RETRIEVED_CONTEXT"

    # Hindi query test
    res_hi = rag_chatbot.answer_query("क्या अगले 30 मिनट में आंधी या बिजली का खतरा है?", block_context=block_ctx, lang="hi")
    assert len(res_hi["answer"]) > 10


def test_emergency_crowd_override():
    # Model predicted safe (prob_break=0.10, prob_storm=0.10 -> GREEN)
    # But crowd reports 4 heavy_rain observations
    res = fusion_engine.compute_risk(
        prob_break=0.10,
        prob_storm=0.10,
        crowd_reports_count=4,
        crowd_report_type="heavy_rain"
    )
    assert res["is_override_triggered"] is True
    assert res["risk_tier"] == "RED"
    assert "OVERRIDE" in res["tier_label_en"]


def test_model_health_and_drift_endpoint():
    response = client.get("/api/health/model")
    assert response.status_code == 200
    data = response.json()
    assert "feature_drift_results" in data
    assert "model_a_health" in data
    assert "imd_benchmark_health" in data
