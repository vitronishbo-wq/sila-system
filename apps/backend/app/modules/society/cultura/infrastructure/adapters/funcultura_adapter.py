from __future__ import annotations
from typing import Any
import httpx
from apps.backend.app.modules.society.cultura.infrastructure.resilience.circuit_breaker import circuit_breaker

class FunculturaAdapter:

    def __init__(self, base_url: str | None=None, api_key: str | None=None) -> None:
        self.base_url = (base_url or '').strip().rstrip('/')
        self.api_key = api_key
        self._client = httpx.AsyncClient(timeout=10.0)

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            return {}
        return {'Authorization': f'Bearer {self.api_key}'}

    @circuit_breaker(name='cultura_funcultura', failure_threshold=3, recovery_timeout=60)
    async def reservar_orcamento(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.base_url:
            return {'status': 'simulado', 'reserva_id': 'FUNC-RESERVA-001'}
        response = await self._client.post(f'{self.base_url}/reservas', json=payload, headers=self._headers())
        response.raise_for_status()
        return response.json()

    @circuit_breaker(name='cultura_funcultura', failure_threshold=3, recovery_timeout=60)
    async def liberar_pagamento(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.base_url:
            return {'status': 'simulado', 'pagamento_id': 'FUNC-PAG-001'}
        response = await self._client.post(f'{self.base_url}/pagamentos', json=payload, headers=self._headers())
        response.raise_for_status()
        return response.json()