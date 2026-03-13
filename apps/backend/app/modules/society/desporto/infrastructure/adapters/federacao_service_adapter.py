from __future__ import annotations
import httpx
from apps.backend.app.modules.society.desporto.application.ports.federacao_service_port import FederacaoServicePort
from apps.backend.app.modules.society.desporto.infrastructure.resilience.circuit_breaker import circuit_breaker
from apps.backend.app.modules.society.desporto.infrastructure.resilience.retry import with_retry

class FederacaoServiceAdapter(FederacaoServicePort):

    def __init__(self, base_url: str | None=None, api_key: str | None=None) -> None:
        self.base_url = (base_url or '').strip().rstrip('/')
        self.api_key = api_key
        self._client = httpx.AsyncClient(timeout=10.0)

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            return {}
        return {'Authorization': f'Bearer {self.api_key}'}

    @with_retry(attempts=3, backoff_seconds=0.5)
    @circuit_breaker(name='desporto_federacao', failure_threshold=3, recovery_timeout=60)
    async def validar_clube_federado(self, codigo_clube: str) -> bool:
        if not self.base_url:
            return True
        response = await self._client.get(f'{self.base_url}/clubes/{codigo_clube}/federado', headers=self._headers())
        if response.status_code == 404:
            return False
        response.raise_for_status()
        payload = response.json()
        return bool(payload.get('federado', False))