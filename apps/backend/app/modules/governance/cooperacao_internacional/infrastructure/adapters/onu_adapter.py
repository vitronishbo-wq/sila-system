from __future__ import annotations
from datetime import date
from typing import Any
import httpx
from apps.backend.app.modules.governance.cooperacao_internacional.infrastructure.resilience.circuit_breaker import circuit_breaker

class ONUAdapter:

    def __init__(self, base_url: str | None=None, api_key: str | None=None) -> None:
        self.base_url = (base_url or '').strip().rstrip('/')
        self.api_key = api_key
        self._client = httpx.AsyncClient(timeout=10.0)

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            return {}
        return {'Authorization': f'Bearer {self.api_key}'}

    @circuit_breaker(name='cooperacao_onu', failure_threshold=3, recovery_timeout=60)
    async def registrar_tratado(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.base_url:
            return {'status': 'simulado', 'numero': payload.get('numero')}
        response = await self._client.post(f'{self.base_url}/treaties/register', json=payload, headers=self._headers())
        response.raise_for_status()
        return response.json()

    @circuit_breaker(name='cooperacao_onu', failure_threshold=3, recovery_timeout=60)
    async def registrar_extincao(self, *, numero_acordo: str, data_extincao: date) -> dict[str, Any]:
        if not self.base_url:
            return {'status': 'simulado', 'numero': numero_acordo}
        response = await self._client.post(f'{self.base_url}/treaties/{numero_acordo}/terminate', json={'data_extincao': data_extincao.isoformat()}, headers=self._headers())
        response.raise_for_status()
        return response.json()