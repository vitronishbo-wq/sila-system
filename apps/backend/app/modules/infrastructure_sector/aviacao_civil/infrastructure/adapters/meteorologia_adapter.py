from __future__ import annotations
from datetime import datetime
from typing import Any
import httpx
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.infrastructure.resilience.circuit_breaker import circuit_breaker

class MeteorologiaAdapter:

    def __init__(self, base_url: str | None=None, api_key: str | None=None) -> None:
        self.base_url = (base_url or '').strip().rstrip('/')
        self.api_key = api_key
        self._client = httpx.AsyncClient(timeout=10.0)

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            return {}
        return {'Authorization': f'Bearer {self.api_key}'}

    @circuit_breaker(name='aviacao_meteorologia', failure_threshold=3, recovery_timeout=20)
    async def consultar_rota(self, *, origem: Any, destino: Any, data_hora: datetime) -> dict[str, Any]:
        if not self.base_url:
            return {'origem': str(origem), 'destino': str(destino), 'data_hora': data_hora.isoformat(), 'condicao': 'favoravel', 'vento_kts': 12}
        response = await self._client.get(f'{self.base_url}/forecast/rota', params={'origem': str(origem), 'destino': str(destino), 'data_hora': data_hora.isoformat()}, headers=self._headers())
        response.raise_for_status()
        return response.json()