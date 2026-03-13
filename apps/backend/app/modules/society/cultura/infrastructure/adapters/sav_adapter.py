from __future__ import annotations
from typing import Any
import httpx
from app.modules.society.cultura.infrastructure.resilience.circuit_breaker import circuit_breaker

class SavAdapter:

    def __init__(self, base_url: str | None=None, api_key: str | None=None) -> None:
        self.base_url = (base_url or '').strip().rstrip('/')
        self.api_key = api_key
        self._client = httpx.AsyncClient(timeout=10.0)

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            return {}
        return {'Authorization': f'Bearer {self.api_key}'}

    @circuit_breaker(name='cultura_sav', failure_threshold=3, recovery_timeout=60)
    async def sincronizar_bilheteria(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.base_url:
            return {'status': 'simulado', 'itens': len(payload.get('itens', []))}
        response = await self._client.post(f'{self.base_url}/bilheteria/sincronizar', json=payload, headers=self._headers())
        response.raise_for_status()
        return response.json()

    @circuit_breaker(name='cultura_sav', failure_threshold=3, recovery_timeout=60)
    async def obter_resumo_vendas(self, evento_externo_id: str) -> dict[str, Any]:
        if not self.base_url:
            return {'status': 'simulado', 'evento_externo_id': evento_externo_id, 'valor_total': 0}
        response = await self._client.get(f'{self.base_url}/vendas/{evento_externo_id}/resumo', headers=self._headers())
        response.raise_for_status()
        return response.json()