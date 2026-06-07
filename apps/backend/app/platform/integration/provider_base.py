import asyncio
import logging
import time
from abc import ABC, abstractmethod
from typing import Any, Optional

import httpx

from apps.backend.app.platform.integration.provider_registry import ProviderRegistry

logger = logging.getLogger(__name__)

RETRYABLE_STATUSES = {429, 500, 502, 503, 504}
MAX_RETRIES = 3
BASE_BACKOFF = 5
MAX_BACKOFF = 120


class ProviderBase(ABC):
    provider_name: str = ""

    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or ""
        self._client = httpx.AsyncClient(timeout=timeout)

    @abstractmethod
    async def health_check(self) -> dict[str, Any]:
        ...

    async def _request(
        self,
        method: str,
        path: str,
        json_data: Optional[dict] = None,
        headers: Optional[dict[str, str]] = None,
        _retry: int = 0,
    ) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        start = time.monotonic()
        try:
            response = await self._client.request(
                method, url, headers=headers, json=json_data,
            )
            latency = time.monotonic() - start

            if response.status_code == 404:
                ProviderRegistry.record_error(self.provider_name, latency, "not_found")
                return {"status": "not_found", "error": str(response.text)}

            if response.status_code == 401:
                ProviderRegistry.record_error(self.provider_name, latency, "authentication_failed")
                return {"status": "error", "error": "authentication_failed"}

            if response.status_code in RETRYABLE_STATUSES and _retry < MAX_RETRIES:
                delay = _backoff_seconds(_retry)
                logger.warning(
                    "%s retry status=%d attempt=%d delay=%.1f",
                    self.provider_name, response.status_code, _retry + 1, delay,
                )
                await asyncio.sleep(delay)
                ProviderRegistry.record_error(self.provider_name, latency, f"retryable_{response.status_code}")
                return await self._request(method, path, json_data, headers, _retry=_retry + 1)

            if response.status_code >= 400:
                ProviderRegistry.record_error(self.provider_name, latency, f"error_{response.status_code}")
                return {"status": "error", "error": response.text}

            result = response.json()
            ProviderRegistry.record_success(self.provider_name, latency)
            return result

        except httpx.RequestError as exc:
            latency = time.monotonic() - start
            if _retry < MAX_RETRIES:
                delay = _backoff_seconds(_retry)
                logger.warning(
                    "%s retry attempt=%d delay=%.1f error=%s",
                    self.provider_name, _retry + 1, delay, exc,
                )
                await asyncio.sleep(delay)
                return await self._request(method, path, json_data, headers, _retry=_retry + 1)
            ProviderRegistry.record_error(self.provider_name, latency, str(exc))
            return {"status": "error", "error": str(exc)}

    async def close(self):
        await self._client.aclose()


def _backoff_seconds(retry: int) -> float:
    delay = min(BASE_BACKOFF * (2 ** retry), MAX_BACKOFF)
    jitter = delay * 0.1
    return delay + jitter


__all__ = ["ProviderBase", "RETRYABLE_STATUSES", "MAX_RETRIES", "BASE_BACKOFF", "MAX_BACKOFF"]
