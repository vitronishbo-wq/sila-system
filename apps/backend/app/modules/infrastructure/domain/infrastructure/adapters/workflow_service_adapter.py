from __future__ import annotations
import os
from uuid import UUID
import httpx
from apps.backend.app.modules.infrastructure.application.ports.workflow_service_port import WorkflowServicePort
from apps.backend.app.modules.infrastructure.infrastructure.observability.tracing import start_span
from apps.backend.app.modules.infrastructure.infrastructure.resilience.bulkhead import AsyncBulkhead
from apps.backend.app.modules.infrastructure.infrastructure.resilience.circuit_breaker import CircuitBreaker
from apps.backend.app.modules.infrastructure.infrastructure.resilience.rate_limit import AsyncRateLimiter
from apps.backend.app.modules.infrastructure.infrastructure.resilience.retry import retry
from apps.backend.app.modules.infrastructure.infrastructure.resilience.timeout import with_timeout

class WorkflowServiceAdapter(WorkflowServicePort):

    def __init__(self, *, base_url: str | None=None, circuit_breaker: CircuitBreaker | None=None) -> None:
        self._base_url = (base_url or os.environ.get('WORKFLOW_BASE_URL') or '').rstrip('/')
        self._circuit_breaker = circuit_breaker or CircuitBreaker()
        self._timeout_seconds = float(os.environ.get('OP_WORKFLOW_TIMEOUT_SECONDS', '5'))
        self._bulkhead = AsyncBulkhead(limit=int(os.environ.get('OP_WORKFLOW_BULKHEAD_LIMIT', '25')))
        self._rate_limiter = AsyncRateLimiter(rate=int(os.environ.get('OP_WORKFLOW_RATE_LIMIT', '600')), per_seconds=60.0)

    async def iniciar_fluxo(self, *, entidade: str, referencia_id: UUID, contexto: dict) -> str:
        if self._circuit_breaker.is_open():
            raise RuntimeError('Workflow indisponivel (circuito aberto)')
        payload = {'entidade': entidade, 'referencia_id': str(referencia_id), 'contexto': contexto}

        async def operation() -> str:
            if not self._base_url:
                return f'WF-{str(referencia_id)[:8].upper()}'
            await self._rate_limiter.acquire()
            async with self._bulkhead:
                with start_span('obras_publicas.workflow.iniciar_fluxo'):
                    async with httpx.AsyncClient(timeout=self._timeout_seconds) as client:
                        response = await with_timeout(client.post(f'{self._base_url}/workflow/instancias', json=payload), timeout_seconds=self._timeout_seconds)
                        response.raise_for_status()
                        body = response.json() if response.content else {}
                        return str(body.get('workflow_id') or body.get('id') or '')
        try:
            workflow_id = await retry(operation, attempts=3, base_delay_seconds=1.0)
            self._circuit_breaker.record_success()
            return workflow_id or f'WF-{str(referencia_id)[:8].upper()}'
        except Exception:
            self._circuit_breaker.record_failure()
            raise

    async def registrar_evento(self, *, workflow_id: str, evento: str, payload: dict) -> None:
        if self._circuit_breaker.is_open():
            raise RuntimeError('Workflow indisponivel (circuito aberto)')
        request_payload = {'evento': evento, 'payload': payload}

        async def operation() -> None:
            if not self._base_url:
                return
            await self._rate_limiter.acquire()
            async with self._bulkhead:
                with start_span('obras_publicas.workflow.registrar_evento'):
                    async with httpx.AsyncClient(timeout=self._timeout_seconds) as client:
                        response = await with_timeout(client.post(f'{self._base_url}/workflow/instancias/{workflow_id}/eventos', json=request_payload), timeout_seconds=self._timeout_seconds)
                        response.raise_for_status()
        try:
            await retry(operation, attempts=3, base_delay_seconds=1.0)
            self._circuit_breaker.record_success()
        except Exception:
            self._circuit_breaker.record_failure()
            raise
