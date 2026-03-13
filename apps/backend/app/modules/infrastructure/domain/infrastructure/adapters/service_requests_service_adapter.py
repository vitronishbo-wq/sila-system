from __future__ import annotations
import os
import httpx
from app.modules.infrastructure.application.ports.service_requests_service_port import ServiceRequestsServicePort
from app.modules.infrastructure.infrastructure.observability.tracing import start_span
from app.modules.infrastructure.infrastructure.resilience.bulkhead import AsyncBulkhead
from app.modules.infrastructure.infrastructure.resilience.circuit_breaker import CircuitBreaker
from app.modules.infrastructure.infrastructure.resilience.rate_limit import AsyncRateLimiter
from app.modules.infrastructure.infrastructure.resilience.retry import retry
from app.modules.infrastructure.infrastructure.resilience.timeout import with_timeout

class ServiceRequestsServiceAdapter(ServiceRequestsServicePort):

    def __init__(self, *, base_url: str | None=None, circuit_breaker: CircuitBreaker | None=None) -> None:
        self._base_url = (base_url or os.environ.get('SERVICE_REQUESTS_BASE_URL') or '').rstrip('/')
        self._circuit_breaker = circuit_breaker or CircuitBreaker()
        self._timeout_seconds = float(os.environ.get('OP_SERVICE_REQUESTS_TIMEOUT_SECONDS', '5'))
        self._bulkhead = AsyncBulkhead(limit=int(os.environ.get('OP_SERVICE_REQUESTS_BULKHEAD_LIMIT', '25')))
        self._rate_limiter = AsyncRateLimiter(rate=int(os.environ.get('OP_SERVICE_REQUESTS_RATE_LIMIT', '600')), per_seconds=60.0)

    async def abrir_solicitacao(self, payload: dict) -> str:
        if self._circuit_breaker.is_open():
            raise RuntimeError('Service Requests indisponivel (circuito aberto)')

        async def operation() -> str:
            if not self._base_url:
                return 'SRQ-PENDING'
            await self._rate_limiter.acquire()
            async with self._bulkhead:
                with start_span('obras_publicas.service_requests.post'):
                    async with httpx.AsyncClient(timeout=self._timeout_seconds) as client:
                        response = await with_timeout(client.post(f'{self._base_url}/service-requests', json=payload), timeout_seconds=self._timeout_seconds)
                        response.raise_for_status()
                        body = response.json() if response.content else {}
                        return str(body.get('id') or body.get('request_id') or 'SRQ-PENDING')
        try:
            result = await retry(operation, attempts=3, base_delay_seconds=1.0)
            self._circuit_breaker.record_success()
            return result
        except Exception:
            self._circuit_breaker.record_failure()
            raise
