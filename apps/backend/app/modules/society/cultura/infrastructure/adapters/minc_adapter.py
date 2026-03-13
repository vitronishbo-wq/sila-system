from __future__ import annotations
from typing import Any
import httpx
from app.modules.society.cultura.infrastructure.resilience.circuit_breaker import circuit_breaker

class MincAdapter:

    def __init__(self, base_url: str | None=None, api_key: str | None=None) -> None:
        self.base_url = (base_url or '').strip().rstrip('/')
        self.api_key = api_key
        self._client = httpx.AsyncClient(timeout=10.0)

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            return {}
        return {'Authorization': f'Bearer {self.api_key}'}

    @circuit_breaker(name='cultura_minc', failure_threshold=3, recovery_timeout=60)
    async def publicar_edital(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.base_url:
            return {'status': 'simulado', 'numero': payload.get('numero')}
        response = await self._client.post(f'{self.base_url}/editais', json=payload, headers=self._headers())
        response.raise_for_status()
        return response.json()

    @circuit_breaker(name='cultura_minc', failure_threshold=3, recovery_timeout=60)
    async def reportar_execucao_projeto(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.base_url:
            return {'status': 'simulado', 'codigo_projeto': payload.get('codigo_projeto')}
        response = await self._client.post(f'{self.base_url}/projetos/execucao', json=payload, headers=self._headers())
        response.raise_for_status()
        return response.json()