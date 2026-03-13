from __future__ import annotations
from typing import Any
import httpx
from app.modules.infrastructure_sector.aviacao_civil.infrastructure.resilience.circuit_breaker import circuit_breaker

class DeceaAdapter:

    def __init__(self, base_url: str | None=None, api_key: str | None=None) -> None:
        self.base_url = (base_url or '').strip().rstrip('/')
        self.api_key = api_key
        self._client = httpx.AsyncClient(timeout=10.0)

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            return {}
        return {'Authorization': f'Bearer {self.api_key}'}

    @circuit_breaker(name='aviacao_decea', failure_threshold=3, recovery_timeout=30)
    async def registrar_voo(self, dados: dict[str, Any]) -> dict[str, Any]:
        if not self.base_url:
            return {'status': 'simulado', 'numero_voo': dados.get('numero_voo')}
        response = await self._client.post(f'{self.base_url}/voos', json=dados, headers=self._headers())
        response.raise_for_status()
        return response.json()

    @circuit_breaker(name='aviacao_decea', failure_threshold=3, recovery_timeout=30)
    async def consultar_posicao(self, numero_voo: str) -> dict[str, Any] | None:
        if not self.base_url:
            return {'numero_voo': numero_voo, 'desviado': False, 'atraso_previsto': 0}
        response = await self._client.get(f'{self.base_url}/voos/{numero_voo}/posicao', headers=self._headers())
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()