from __future__ import annotations

from datetime import datetime
from typing import Any

import httpx

from apps.backend.app.modules.governance.cooperacao_internacional.infrastructure.resilience.circuit_breaker import (
    circuit_breaker,
)


class CambioAdapter:
    def __init__(self, base_url: str | None = None, api_key: str | None = None) -> None:
        self.base_url = (base_url or "").strip().rstrip("/")
        self.api_key = api_key
        self._client = httpx.AsyncClient(timeout=10.0)

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            return {}
        return {"Authorization": f"Bearer {self.api_key}"}

    @circuit_breaker(name="cooperacao_cambio", failure_threshold=3, recovery_timeout=20)
    async def cotar(self, *, moeda_origem: str, moeda_destino: str) -> dict[str, Any]:
        if not self.base_url:
            return {
                "moeda_origem": moeda_origem,
                "moeda_destino": moeda_destino,
                "taxa": 1.0,
                "timestamp": datetime.utcnow().isoformat(),
            }
        response = await self._client.get(
            f"{self.base_url}/fx/rate",
            params={"from": moeda_origem, "to": moeda_destino},
            headers=self._headers(),
        )
        response.raise_for_status()
        return response.json()
