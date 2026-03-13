from __future__ import annotations
import os
from decimal import Decimal
from typing import Any
import httpx
from app.modules.infrastructure.infrastructure.observability.tracing import start_span
from app.modules.infrastructure.infrastructure.resilience.bulkhead import AsyncBulkhead
from app.modules.infrastructure.infrastructure.resilience.circuit_breaker import CircuitBreaker
from app.modules.infrastructure.infrastructure.resilience.rate_limit import AsyncRateLimiter
from app.modules.infrastructure.infrastructure.resilience.retry import retry
from app.modules.infrastructure.infrastructure.resilience.timeout import with_timeout

class TCUAdapter:

    def __init__(self, tenant_id: str, *, base_url: str | None=None, circuit_breaker: CircuitBreaker | None=None) -> None:
        self.tenant_id = tenant_id
        self.base_url = (base_url or os.environ.get('TCU_BASE_URL') or '').rstrip('/')
        self._circuit_breaker = circuit_breaker or CircuitBreaker()
        self._timeout_seconds = float(os.environ.get('OP_TCU_TIMEOUT_SECONDS', '5'))
        self._bulkhead = AsyncBulkhead(limit=int(os.environ.get('OP_TCU_BULKHEAD_LIMIT', '15')))
        self._rate_limiter = AsyncRateLimiter(rate=int(os.environ.get('OP_TCU_RATE_LIMIT', '300')), per_seconds=60.0)

    async def registrar_aditivo(self, *, obra_id: str, valor_adicional: Decimal, idempotency_key: str, correlation_id: str) -> dict[str, Any]:
        if self._circuit_breaker.is_open():
            raise RuntimeError('TCU indisponivel (circuito aberto)')
        headers = {'X-Tenant-ID': self.tenant_id, 'X-Correlation-ID': correlation_id, 'Idempotency-Key': idempotency_key}
        payload = {'obra_id': obra_id, 'valor_adicional': str(valor_adicional)}

        async def operation() -> dict[str, Any]:
            if not self.base_url:
                return {'status': 'accepted', 'mocked': True, 'payload': payload}
            await self._rate_limiter.acquire()
            async with self._bulkhead:
                with start_span('obras_publicas.tcu.post', {'tenant_id': self.tenant_id, 'correlation_id': correlation_id}):
                    async with httpx.AsyncClient(timeout=self._timeout_seconds) as client:
                        response = await with_timeout(client.post(f'{self.base_url}/integracoes/obras/aditivos', json=payload, headers=headers), timeout_seconds=self._timeout_seconds)
                        response.raise_for_status()
                        return response.json() if response.content else {'status': 'ok'}
        try:
            result = await retry(operation, attempts=3, base_delay_seconds=1.0)
            self._circuit_breaker.record_success()
            return result
        except Exception:
            self._circuit_breaker.record_failure()
            raise
