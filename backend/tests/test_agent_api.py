"""
Pytest Test Suite for Agent37 Kisan Saarthi Layer.
Validates:
1. Success: Agent37 returns status 'completed' and non-empty output -> source='agent37'
2. Timeout: Network timeout triggers graceful fallback to deterministic RAG -> source='rag_fallback'
3. Failed Status: Agent37 HTTP 200 with status 'failed' triggers RAG fallback -> source='rag_fallback'
4. Empty Output: Agent37 returning whitespace or empty output triggers RAG fallback -> source='rag_fallback'
5. Unconfigured: When credentials are not set, instant RAG fallback -> source='rag_fallback'
6. Query Too Long: Query > 500 characters rejected with HTTP 422
7. Status Endpoint: GET /api/agent/status returns booleans only (configured, healthy)
8. Tool Key Unconfigured: Returns HTTP 503 (disabled) when AGENT_TOOLS_KEY is empty
9. Tool Key Missing: Returns HTTP 401
10. Tool Key Wrong: Returns HTTP 401
11. Tool Key Right: Returns HTTP 200 with read-only data
"""

import pytest
import httpx
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.core.config import settings
from backend.app.agents.agent37_client import agent37_client

client = TestClient(app)


# ==============================================================================
# Helper Mock Transports
# ==============================================================================

class MockHandlerTransport(httpx.AsyncBaseTransport):
    """Custom httpx Async Transport that routes calls to a handler function."""
    def __init__(self, handler):
        self.handler = handler

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        return self.handler(request)


# ==============================================================================
# Tests
# ==============================================================================

def test_agent_status_endpoint_unconfigured(monkeypatch):
    """When credentials are unset, /api/agent/status returns booleans only."""
    monkeypatch.setattr(settings, "AGENT37_API_KEY", "")
    monkeypatch.setattr(settings, "AGENT37_INSTANCE_URL", "")
    monkeypatch.setattr(settings, "AGENT37_INSTANCE_ID", "")
    agent37_client._api_key = None
    agent37_client._instance_url = None
    agent37_client._instance_id = None

    resp = client.get("/api/agent/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data == {"configured": False, "healthy": False}
    assert isinstance(data["configured"], bool)
    assert isinstance(data["healthy"], bool)


def test_agent_status_endpoint_healthy(monkeypatch):
    """When configured and health check succeeds, returns configured=True, healthy=True."""
    monkeypatch.setattr(settings, "AGENT37_API_KEY", "sk_live_test_123")
    monkeypatch.setattr(settings, "AGENT37_INSTANCE_URL", "https://mock-inst.agent37.app")

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers.get("X-Agent37-Key") == "sk_live_test_123"
        return httpx.Response(200, json={"ok": True, "healthy": True, "agent": "hermes"})

    agent37_client._transport = MockHandlerTransport(handler)

    try:
        resp = client.get("/api/agent/status")
        assert resp.status_code == 200
        data = resp.json()
        assert data == {"configured": True, "healthy": True}
    finally:
        agent37_client._transport = None


def test_agent_chat_unconfigured_fallback(monkeypatch):
    """When AGENT37 is not configured, /api/agent/chat returns deterministic RAG fallback."""
    monkeypatch.setattr(settings, "AGENT37_API_KEY", "")
    monkeypatch.setattr(settings, "AGENT37_INSTANCE_URL", "")
    monkeypatch.setattr(settings, "AGENT37_INSTANCE_ID", "")
    agent37_client._api_key = None
    agent37_client._instance_url = None
    agent37_client._instance_id = None

    resp = client.post(
        "/api/agent/chat",
        json={"query": "Should I sow cotton now?", "block_id": "MH_YVT_01", "language": "en"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["source"] == "rag_fallback"
    assert "answer" in data and len(data["answer"]) > 0
    assert "response" in data
    assert data["language"] == "en"
    assert data["grounding_status"] == "STRICTLY_GROUNDED_IN_RETRIEVED_CONTEXT"


def test_agent_chat_success(monkeypatch):
    """When Agent37 succeeds with status 'completed', returns source='agent37'."""
    monkeypatch.setattr(settings, "AGENT37_API_KEY", "sk_live_test_456")
    monkeypatch.setattr(settings, "AGENT37_INSTANCE_URL", "https://mock-inst.agent37.app")

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers.get("X-Agent37-Key") == "sk_live_test_456"
        return httpx.Response(
            200,
            json={
                "id": "resp_99182",
                "session_id": "sess_farm_01",
                "status": "completed",
                "output_text": "Conditions in Pusad are favorable for cotton sowing. Soil moisture is adequate.",
                "usage": {"input_tokens": 80, "output_tokens": 18}
            }
        )

    agent37_client._transport = MockHandlerTransport(handler)

    try:
        resp = client.post(
            "/api/agent/chat",
            json={"query": "Can I sow cotton?", "block_id": "MH_YVT_01", "language": "en"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["source"] == "agent37"
        assert "Conditions in Pusad are favorable" in data["answer"]
        assert data["response"] == data["answer"]
        assert data["session_id"] == "sess_farm_01"
        assert data["agent37"]["status"] == "completed"
    finally:
        agent37_client._transport = None


def test_agent_chat_timeout_fallback(monkeypatch):
    """When Agent37 times out, it gracefully falls back to deterministic RAG."""
    monkeypatch.setattr(settings, "AGENT37_API_KEY", "sk_live_test_456")
    monkeypatch.setattr(settings, "AGENT37_INSTANCE_URL", "https://mock-inst.agent37.app")

    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.TimeoutException("Connection timed out after 8.0s")

    agent37_client._transport = MockHandlerTransport(handler)

    try:
        resp = client.post(
            "/api/agent/chat",
            json={"query": "Should I sow cotton now?", "block_id": "MH_YVT_01", "language": "en"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["source"] == "rag_fallback"
        assert "answer" in data and len(data["answer"]) > 0
    finally:
        agent37_client._transport = None


def test_agent_chat_failed_status_fallback(monkeypatch):
    """When Agent37 returns HTTP 200 but status='failed', it falls back to RAG."""
    monkeypatch.setattr(settings, "AGENT37_API_KEY", "sk_live_test_456")
    monkeypatch.setattr(settings, "AGENT37_INSTANCE_URL", "https://mock-inst.agent37.app")

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "id": "resp_fail_01",
                "session_id": "sess_farm_02",
                "status": "failed",
                "error": {"code": "model_overloaded", "message": "Upstream model rate limit"}
            }
        )

    agent37_client._transport = MockHandlerTransport(handler)

    try:
        resp = client.post(
            "/api/agent/chat",
            json={"query": "Should I sow cotton now?", "block_id": "MH_YVT_01", "language": "en"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["source"] == "rag_fallback"
        assert len(data["answer"]) > 0
    finally:
        agent37_client._transport = None


def test_agent_chat_empty_output_fallback(monkeypatch):
    """When Agent37 returns whitespace/empty output_text, it falls back to RAG."""
    monkeypatch.setattr(settings, "AGENT37_API_KEY", "sk_live_test_456")
    monkeypatch.setattr(settings, "AGENT37_INSTANCE_URL", "https://mock-inst.agent37.app")

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "id": "resp_empty_01",
                "session_id": "sess_farm_03",
                "status": "completed",
                "output_text": "   "
            }
        )

    agent37_client._transport = MockHandlerTransport(handler)

    try:
        resp = client.post(
            "/api/agent/chat",
            json={"query": "Should I sow cotton now?", "block_id": "MH_YVT_01", "language": "en"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["source"] == "rag_fallback"
        assert len(data["answer"]) > 0
    finally:
        agent37_client._transport = None


def test_agent_chat_query_too_long():
    """Queries exceeding 500 characters must be rejected with HTTP 422."""
    long_query = "A" * 501
    resp = client.post(
        "/api/agent/chat",
        json={"query": long_query, "block_id": "MH_YVT_01", "language": "en"}
    )
    assert resp.status_code == 422


# ==============================================================================
# Agent Tools Security Tests
# ==============================================================================

def test_agent_tools_key_unconfigured_503(monkeypatch):
    """When AGENT_TOOLS_KEY is empty/unset, tool endpoints return HTTP 503."""
    monkeypatch.setattr(settings, "AGENT_TOOLS_KEY", "")

    resp = client.get("/api/agent-tools/alerts")
    assert resp.status_code == 503
    assert "disabled" in resp.json()["detail"].lower()


def test_agent_tools_key_missing_401(monkeypatch):
    """When AGENT_TOOLS_KEY is set but X-Tools-Key header is missing, returns HTTP 401."""
    monkeypatch.setattr(settings, "AGENT_TOOLS_KEY", "correct_secret_key_12345")

    resp = client.get("/api/agent-tools/alerts")
    assert resp.status_code == 401
    assert "Invalid or missing" in resp.json()["detail"]


def test_agent_tools_key_wrong_401(monkeypatch):
    """When X-Tools-Key is incorrect, returns HTTP 401."""
    monkeypatch.setattr(settings, "AGENT_TOOLS_KEY", "correct_secret_key_12345")

    resp = client.get("/api/agent-tools/alerts", headers={"X-Tools-Key": "wrong_key_999"})
    assert resp.status_code == 401
    assert "Invalid or missing" in resp.json()["detail"]


def test_agent_tools_key_right_success(monkeypatch):
    """When X-Tools-Key matches AGENT_TOOLS_KEY, returns 200 with read-only data."""
    secret_key = "correct_secret_key_12345"
    monkeypatch.setattr(settings, "AGENT_TOOLS_KEY", secret_key)
    headers = {"X-Tools-Key": secret_key}

    # 1. Alerts tool
    resp_alerts = client.get("/api/agent-tools/alerts", headers=headers)
    assert resp_alerts.status_code == 200
    assert "alerts" in resp_alerts.json()

    # 2. Forecast tool
    resp_fc = client.get("/api/agent-tools/forecast/MH_YVT_01", headers=headers)
    assert resp_fc.status_code == 200
    data_fc = resp_fc.json()
    assert data_fc["block_id"] == "MH_YVT_01"
    assert "latest_risk_tier" in data_fc

    # 3. Crowd reports tool
    resp_cr = client.get("/api/agent-tools/crowd-reports", headers=headers)
    assert resp_cr.status_code == 200
    assert "reports" in resp_cr.json()

    # 4. Advisory tool
    resp_adv = client.get("/api/agent-tools/advisory/MH_YVT_01?crop=cotton&stage=sowing", headers=headers)
    assert resp_adv.status_code == 200
    assert "advisory" in resp_adv.json()
