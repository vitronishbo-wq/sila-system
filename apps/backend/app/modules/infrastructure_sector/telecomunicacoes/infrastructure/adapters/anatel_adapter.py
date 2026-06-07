from __future__ import annotations

import os
from collections.abc import Mapping
from typing import Any

import httpx

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.resilience.circuit_breaker import (
    CircuitBreaker,
)


class AnatelAdapter:
    """Gateway para integracao regulatoria com a Anatel."""

    def __init__(
        self,
        *,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout_seconds: float = 10.0,
        failure_threshold: int = 3,
        recovery_timeout: int = 30,
        client: Any | None = None,
    ) -> None:
        self._base_url = (
            base_url or os.getenv("TELECOM_ANATEL_BASE_URL") or "http://127.0.0.1:8090"
        ).rstrip("/")
        self._api_key = api_key or os.getenv("TELECOM_ANATEL_API_KEY")
        self._timeout_seconds = timeout_seconds
        self._client = client
        self._breaker = CircuitBreaker(
            failure_threshold=failure_threshold, recovery_timeout=recovery_timeout
        )
        self._guarded_request = self._breaker(self._request)

    async def registrar_reclamacao(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        return await self._guarded_request(
            method="POST", path="/api/v1/reclamacoes", payload=dict(payload)
        )

    async def registrar_alerta_qualidade(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        return await self._guarded_request(
            method="POST", path="/api/v1/qualidade/alertas", payload=dict(payload)
        )

    async def _request(self, *, method: str, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self._base_url}/{path.lstrip('/')}"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"
        response = await self._send_http(method=method, url=url, payload=payload, headers=headers)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise RuntimeError("Falha HTTP ao comunicar com a Anatel") from exc
        content_type = (response.headers or {}).get("content-type", "").lower()
        if not response.content:
            return {"status": "accepted"}
        if "application/json" in content_type:
            body = response.json()
            if isinstance(body, dict):
                return body
            return {"data": body}
        return {"raw": response.text}

    async def _send_http(
        self, *, method: str, url: str, payload: dict[str, Any], headers: dict[str, str]
    ) -> httpx.Response:
        try:
            if self._client is not None:
                return await self._client.request(
                    method=method,
                    url=url,
                    json=payload,
                    headers=headers,
                    timeout=self._timeout_seconds,
                )
            async with httpx.AsyncClient(timeout=self._timeout_seconds) as client:
                return await client.request(method=method, url=url, json=payload, headers=headers)
        except httpx.HTTPError as exc:
            raise RuntimeError("Falha de comunicacao com a Anatel") from exc
