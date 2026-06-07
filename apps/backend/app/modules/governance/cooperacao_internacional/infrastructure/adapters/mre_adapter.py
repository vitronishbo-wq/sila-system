from __future__ import annotations

from datetime import date
from typing import Any

import httpx

from apps.backend.app.modules.governance.cooperacao_internacional.infrastructure.resilience.circuit_breaker import (
    circuit_breaker,
)


class MREAdapter:
    def __init__(self, base_url: str | None = None, api_key: str | None = None) -> None:
        self.base_url = (base_url or "").strip().rstrip("/")
        self.api_key = api_key
        self._client = httpx.AsyncClient(timeout=10.0)

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            return {}
        return {"Authorization": f"Bearer {self.api_key}"}

    @circuit_breaker(name="cooperacao_mre", failure_threshold=3, recovery_timeout=60)
    async def registrar_acordo(self, dados: dict[str, Any]) -> dict[str, Any]:
        if not self.base_url:
            return {"status": "simulado", "numero": dados.get("numero")}
        response = await self._client.post(
            f"{self.base_url}/acordos", json=dados, headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    @circuit_breaker(name="cooperacao_mre", failure_threshold=3, recovery_timeout=60)
    async def registrar_assinatura(
        self, *, numero_acordo: str, data_assinatura: date, local: str, partes: int
    ) -> dict[str, Any]:
        if not self.base_url:
            return {"status": "simulado", "numero": numero_acordo}
        response = await self._client.post(
            f"{self.base_url}/acordos/{numero_acordo}/assinaturas",
            json={"data_assinatura": data_assinatura.isoformat(), "local": local, "partes": partes},
            headers=self._headers(),
        )
        response.raise_for_status()
        return response.json()
