from __future__ import annotations

from typing import Any
from uuid import UUID

from apps.backend.app.processes.contracts import (
    PedidoBeneficioEvent,
    VerificacaoNifConcluidaEvent,
    VerificacaoSSConcluidaEvent,
    BeneficioAprovadoEvent,
)
from apps.backend.app.core.events.domain_event import DomainEvent


class DefaultEventPublisher:
    """Adapter that exposes `publish_atomic` like EventBusBridge for tests/production.

    In production you can pass an instance of `EventBusBridge` which has the same
    method signature used here. For lightweight tests you can pass a stub with
    `published` and `appended` tracking.
    """

    def __init__(self, event_bus: Any | None = None):
        self._bus = event_bus

    async def publish_atomic(self, event: DomainEvent, **kwargs) -> Any:
        if self._bus and hasattr(self._bus, "publish_atomic"):
            return await self._bus.publish_atomic(event, **kwargs)
        if self._bus and hasattr(self._bus, "publish"):
            await self._bus.publish(event)
            return event
        # No-op fallback
        return event


class BeneficioHandlers:
    def __init__(
        self,
        beneficio_service: object,
        beneficio_repo: object | None = None,
        workflow_engine: object | None = None,
        event_publisher: object | None = None,
    ) -> None:
        self._svc = beneficio_service
        self._repo = beneficio_repo
        self._wf = workflow_engine
        self._publisher = event_publisher or DefaultEventPublisher()

    async def submit(self, *, beneficiario_id: UUID, tipo, valor, programa_social_id: UUID | None = None):
        beneficio = await self._svc.solicitar_beneficio(
            beneficiario_id=beneficiario_id, tipo=tipo, valor=valor, programa_social_id=programa_social_id
        )
        # start workflow
        provider = str(beneficio.id)
        if self._wf:
            self._wf.criar(provider=provider, beneficiario_id=str(beneficio.beneficiario_id))

        # publish process event
        evt = PedidoBeneficioEvent(pedido_id=beneficio.id, beneficiario_id=beneficio.beneficiario_id, dados={"codigo": beneficio.codigo})
        # include causation_id when available (first event has no causation)
        causation = None
        domain_evt = evt.to_domain_event(aggregate_type="Beneficio", aggregate_id=beneficio.id, correlation_id=beneficio.id, causation_id=causation)
        published = await self._publisher.publish_atomic(domain_evt, aggregate_id=beneficio.id, aggregate_type="Beneficio", version=evt.version, metadata=evt.to_payload())
        # record last published event id in workflow wrapper to enable causation propagation
        if self._wf and hasattr(self._wf, "set_last_event"):
            try:
                self._wf.set_last_event(provider, published.event_id)
            except Exception:
                pass
        return beneficio

    async def verify_nif(self, pedido_id: UUID, valid: bool, nif: str | None = None) -> None:
        evt = VerificacaoNifConcluidaEvent(pedido_id=pedido_id, nif=nif, valid=valid)
        causation = None
        if self._wf and hasattr(self._wf, "get_last_event"):
            causation = self._wf.get_last_event(str(pedido_id))
        domain_evt = evt.to_domain_event(aggregate_type="Beneficio", aggregate_id=pedido_id, correlation_id=pedido_id, causation_id=causation)
        published = await self._publisher.publish_atomic(domain_evt, aggregate_id=pedido_id, aggregate_type="Beneficio", version=evt.version, metadata=evt.to_payload())
        if self._wf and hasattr(self._wf, "set_last_event"):
            try:
                self._wf.set_last_event(str(pedido_id), published.event_id)
            except Exception:
                pass
        if not valid and self._svc:
            # reject beneficio
            await self._svc.negar_beneficio(pedido_id, motivo="nif_invalid")

    async def verify_ss(self, pedido_id: UUID, valid: bool, ss_number: str | None = None) -> None:
        evt = VerificacaoSSConcluidaEvent(pedido_id=pedido_id, ss_number=ss_number, valid=valid)
        causation = None
        if self._wf and hasattr(self._wf, "get_last_event"):
            causation = self._wf.get_last_event(str(pedido_id))
        domain_evt = evt.to_domain_event(aggregate_type="Beneficio", aggregate_id=pedido_id, correlation_id=pedido_id, causation_id=causation)
        published = await self._publisher.publish_atomic(domain_evt, aggregate_id=pedido_id, aggregate_type="Beneficio", version=evt.version, metadata=evt.to_payload())
        if self._wf and hasattr(self._wf, "set_last_event"):
            try:
                self._wf.set_last_event(str(pedido_id), published.event_id)
            except Exception:
                pass
        if not valid and self._svc:
            await self._svc.negar_beneficio(pedido_id, motivo="ss_invalid")

    async def approve(self, pedido_id: UUID, valor: float) -> None:
        beneficio = await self._svc.aprovar_beneficio(beneficio_id=pedido_id)
        evt = BeneficioAprovadoEvent(pedido_id=pedido_id, beneficio_id=beneficio.id, valor=float(valor))
        causation = None
        if self._wf and hasattr(self._wf, "get_last_event"):
            causation = self._wf.get_last_event(str(pedido_id))
        domain_evt = evt.to_domain_event(aggregate_type="Beneficio", aggregate_id=pedido_id, correlation_id=pedido_id, causation_id=causation)
        published = await self._publisher.publish_atomic(domain_evt, aggregate_id=pedido_id, aggregate_type="Beneficio", version=evt.version, metadata=evt.to_payload())
        if self._wf and hasattr(self._wf, "set_last_event"):
            try:
                self._wf.set_last_event(str(pedido_id), published.event_id)
            except Exception:
                pass

    async def cancel(self, pedido_id: UUID, motivo: str = "cancelled") -> None:
        await self._svc.encerrar_beneficio(beneficio_id=pedido_id, motivo=motivo)
        # publish a generic cancellation event using VerificacaoSSConcluidaEvent with valid=False for traceability
        evt = VerificacaoSSConcluidaEvent(pedido_id=pedido_id, ss_number=None, valid=False)
        causation = None
        if self._wf and hasattr(self._wf, "get_last_event"):
            causation = self._wf.get_last_event(str(pedido_id))
        domain_evt = evt.to_domain_event(aggregate_type="Beneficio", aggregate_id=pedido_id, correlation_id=pedido_id, causation_id=causation)
        published = await self._publisher.publish_atomic(domain_evt, aggregate_id=pedido_id, aggregate_type="Beneficio", version=evt.version, metadata={"reason": motivo})
        if self._wf and hasattr(self._wf, "set_last_event"):
            try:
                self._wf.set_last_event(str(pedido_id), published.event_id)
            except Exception:
                pass

