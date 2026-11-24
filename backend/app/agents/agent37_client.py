"""
Agent37 Async HTTP Client for Kisan Saarthi Agentic Layer.
Official API Integration:
- Health: GET {instance_url}/v1/health with header X-Agent37-Key; checks healthy == True
- Responses: POST {instance_url}/v1/responses with header X-Agent37-Key; checks status == 'completed'
Strict Rules:
- Typed exceptions for all failure modes
- No secrets in logs (API keys and auth headers are never logged)
- Graceful degradation
"""

import logging
from typing import Dict, Any, Optional
import httpx

from backend.app.core.config import settings

logger = logging.getLogger("navchakra.agents.agent37")


# ==============================================================================
# Typed Exceptions
# ==============================================================================

class Agent37Error(Exception):
    """Base exception for all Agent37 client errors."""
    pass


class Agent37NotConfiguredError(Agent37Error):
    """Raised when Agent37 credentials or instance URL are missing."""
    pass


class Agent37TimeoutError(Agent37Error):
    """Raised when an Agent37 network call exceeds the configured timeout."""
    pass


class Agent37UnavailableError(Agent37Error):
    """Raised when the Agent37 instance is offline, unreachable, or returns a 5xx."""
    pass


class Agent37TurnFailedError(Agent37Error):
    """Raised when an Agent37 turn fails, returns empty output, or status != 'completed'."""
    pass


# ==============================================================================
# Client Implementation
# ==============================================================================

class Agent37Client:
    def __init__(
        self,
        api_key: Optional[str] = None,
        instance_url: Optional[str] = None,
        instance_id: Optional[str] = None,
        timeout_s: Optional[float] = None,
        transport: Optional[httpx.AsyncBaseTransport] = None,
    ):
        self._api_key = api_key
        self._instance_url = instance_url
        self._instance_id = instance_id
        self._timeout_s = timeout_s
        self._transport = transport

    @property
    def api_key(self) -> str:
        return self._api_key or settings.AGENT37_API_KEY or ""

    @property
    def instance_url(self) -> str:
        url = self._instance_url or settings.AGENT37_INSTANCE_URL or ""
        if not url:
            inst_id = self._instance_id or settings.AGENT37_INSTANCE_ID or ""
            if inst_id:
                url = f"https://{inst_id}.agent37.app"
        return url.rstrip("/")

    @property
    def timeout_s(self) -> float:
        if self._timeout_s is not None:
            return self._timeout_s
        return settings.AGENT37_TIMEOUT_S or 8.0

    def is_configured(self) -> bool:
        """Returns True only if both API key and instance URL are configured."""
        return bool(self.api_key.strip() and self.instance_url.strip())

    def _get_headers(self) -> Dict[str, str]:
        """Constructs headers. Note: Key is only attached in outgoing request, never logged."""
        return {
            "X-Agent37-Key": self.api_key.strip(),
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _create_async_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            transport=self._transport,
            timeout=httpx.Timeout(self.timeout_s),
        )

    async def get_health(self) -> bool:
        """
        Probes GET {instance_url}/v1/health with header X-Agent37-Key.
        Returns True if and only if healthy == True.
        """
        if not self.is_configured():
            return False

        url = f"{self.instance_url}/v1/health"
        headers = self._get_headers()

        try:
            async with self._create_async_client() as client:
                resp = await client.get(url, headers=headers)
                if resp.status_code != 200:
                    logger.warning(
                        "Agent37 health check non-200: status=%d on instance=%s",
                        resp.status_code,
                        self.instance_url,
                    )
                    return False
                data = resp.json()
                return bool(data.get("healthy") is True)
        except httpx.TimeoutException:
            logger.warning("Agent37 health check timed out on %s", self.instance_url)
            return False
        except Exception as exc:
            logger.warning("Agent37 health probe error on %s: %s", self.instance_url, type(exc).__name__)
            return False

    async def ask(
        self,
        input_text: str,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Executes a turn on the Agent37 instance via POST {instance_url}/v1/responses.
        Validates that status == 'completed' and output_text is non-empty.
        Raises typed exceptions on any error (no secrets logged).
        """
        if not self.is_configured():
            raise Agent37NotConfiguredError(
                "Agent37 is not configured. AGENT37_API_KEY and AGENT37_INSTANCE_URL required."
            )

        url = f"{self.instance_url}/v1/responses"
        headers = self._get_headers()
        payload: Dict[str, Any] = {
            "input": input_text,
            "stream": False,
        }
        if session_id:
            payload["session_id"] = session_id

        try:
            async with self._create_async_client() as client:
                resp = await client.post(url, headers=headers, json=payload)
        except httpx.TimeoutException as exc:
            logger.error("Agent37 request timed out after %.1fs on %s", self.timeout_s, self.instance_url)
            raise Agent37TimeoutError(f"Agent37 request timed out after {self.timeout_s}s") from exc
        except (httpx.ConnectError, httpx.NetworkError) as exc:
            logger.error("Agent37 network/connection failure on %s", self.instance_url)
            raise Agent37UnavailableError("Agent37 instance unreachable or network failure") from exc
        except Exception as exc:
            logger.error("Agent37 unexpected client error on %s: %s", self.instance_url, type(exc).__name__)
            raise Agent37UnavailableError(f"Agent37 unexpected request error: {type(exc).__name__}") from exc

        # Handle HTTP status codes
        if resp.status_code >= 500:
            logger.error("Agent37 server returned HTTP %d on %s", resp.status_code, self.instance_url)
            raise Agent37UnavailableError(f"Agent37 server returned HTTP {resp.status_code}")
        elif resp.status_code >= 400:
            logger.error("Agent37 client rejected with HTTP %d on %s", resp.status_code, self.instance_url)
            raise Agent37TurnFailedError(f"Agent37 rejected request with HTTP {resp.status_code}")

        try:
            data = resp.json()
        except Exception as exc:
            logger.error("Failed to parse JSON response from Agent37 on %s", self.instance_url)
            raise Agent37TurnFailedError("Invalid JSON received from Agent37") from exc

        # Crucial Agent37 API detail: A turn can settle with HTTP 200 but status == "failed"
        turn_status = data.get("status")
        if turn_status != "completed":
            err_obj = data.get("error") or {}
            err_code = err_obj.get("code", "unknown")
            err_msg = err_obj.get("message", "Turn did not complete successfully")
            logger.warning(
                "Agent37 turn did not complete: status=%s, error_code=%s on %s",
                turn_status,
                err_code,
                self.instance_url,
            )
            raise Agent37TurnFailedError(f"Agent37 turn status '{turn_status}': {err_msg}")

        output_text = data.get("output_text")
        if not output_text or not isinstance(output_text, str) or not output_text.strip():
            logger.warning("Agent37 returned empty output_text on %s", self.instance_url)
            raise Agent37TurnFailedError("Agent37 returned empty output text")

        return {
            "output_text": output_text.strip(),
            "session_id": data.get("session_id"),
            "id": data.get("id"),
            "status": "completed",
            "usage": data.get("usage"),
        }


# Global default instance
agent37_client = Agent37Client()
