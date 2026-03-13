from __future__ import annotations
from datetime import datetime
from typing import Any
from uuid import UUID
import httpx
from apps.backend.app.modules.society.cultura.infrastructure.resilience.circuit_breaker import circuit_breaker

class IphanAdapter:

    def __init__(self, base_url: str | None=None, api_key: str | None=None) -> None:
        self.base_url = (base_url or '').strip().rstrip('/')
        self.api_key = api_key
        self._client = httpx.AsyncClient(timeout=10.0)

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            return {}
        return {'Authorization': f'Bearer {self.api_key}'}

    @circuit_breaker(name='cultura_iphan', failure_threshold=3, recovery_timeout=60)
    async def registrar_bem_tombado(self, dados: dict[str, Any]) -> dict[str, Any]:
        if not self.base_url:
            return {'status': 'simulado', 'codigo_iphan': f'IPHAN-{dados.get('bem_id', 'N/A')}'}
        response = await self._client.post(f'{self.base_url}/bens-tombados', json=dados, headers=self._headers())
        response.raise_for_status()
        return response.json()

    @circuit_breaker(name='cultura_iphan', failure_threshold=3, recovery_timeout=60)
    async def consultar_bem(self, codigo_iphan: str) -> dict[str, Any] | None:
        if not self.base_url:
            return {'codigo_iphan': codigo_iphan, 'status': 'simulado'}
        response = await self._client.get(f'{self.base_url}/bens-tombados/{codigo_iphan}', headers=self._headers())
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    @circuit_breaker(name='cultura_iphan', failure_threshold=3, recovery_timeout=60)
    async def solicitar_tombamento(self, *, bem_id: UUID, justificativa: str, documentacao: list[str]) -> dict[str, Any]:
        payload = {'bem_id': str(bem_id), 'justificativa': justificativa, 'documentacao': documentacao}
        if not self.base_url:
            return {'status': 'simulado', 'protocolo': f'TOMB-{str(bem_id)[:8]}'}
        response = await self._client.post(f'{self.base_url}/solicitacoes-tombamento', json=payload, headers=self._headers())
        response.raise_for_status()
        return response.json()

    @circuit_breaker(name='cultura_iphan', failure_threshold=3, recovery_timeout=60)
    async def registrar_intervencao(self, *, bem_id: UUID, tipo: str, descricao: str, responsavel: str, data_inicio: datetime, data_fim: datetime | None=None) -> dict[str, Any]:
        payload = {'tipo': tipo, 'descricao': descricao, 'responsavel': responsavel, 'data_inicio': data_inicio.isoformat(), 'data_fim': data_fim.isoformat() if data_fim else None}
        if not self.base_url:
            return {'status': 'simulado', 'intervencao_id': f'INT-{str(bem_id)[:8]}'}
        response = await self._client.post(f'{self.base_url}/bens-tombados/{bem_id}/intervencoes', json=payload, headers=self._headers())
        response.raise_for_status()
        return response.json()