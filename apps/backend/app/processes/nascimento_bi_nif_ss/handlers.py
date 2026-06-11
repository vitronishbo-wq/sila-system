from __future__ import annotations

from typing import Any, Dict
from uuid import UUID, uuid4

from apps.backend.app.processes.contracts import (
    RegistoNascimentoCriadoEvent,
    CertidaoEmitidaEvent,
    NIFAtribuidoEvent,
    SSAtribuidoEvent,
    RegistroCanceladoEvent,
)


class DefaultEventPublisher:
    def __init__(self, bus: Any | None = None):
        self._bus = bus

    async def publish_atomic(self, domain_event: Any, **_kwargs) -> Any:
        if self._bus and hasattr(self._bus, "publish_atomic"):
            return await self._bus.publish_atomic(domain_event, **_kwargs)
        return domain_event


class NascimentoHandlers:
    """Handlers for the Nascimento -> BI -> NIF -> SS process.

    This is intentionally lightweight: it publishes domain events via a provided
    publisher and keeps a local causation chain map for the lifecycle of a
    single test/process instance.
    """

    def __init__(self, publisher: Any | None = None) -> None:
        self._publisher = publisher or DefaultEventPublisher()
        self._last_event: Dict[str, UUID] = {}

    async def register_birth(self, dados: dict) -> UUID:
        registro_id = uuid4()
        evt = RegistoNascimentoCriadoEvent(registro_id=registro_id, dados=dados)
        domain_event = evt.to_domain_event(
            aggregate_type="Nascimento", aggregate_id=registro_id, correlation_id=registro_id
        )
        published = await self._publisher.publish_atomic(domain_event, aggregate_id=registro_id, aggregate_type="Nascimento")
        try:
            self._last_event[str(registro_id)] = published.event_id
        except Exception:
            # best-effort: if publisher returns plain DomainEvent-like object
            pass
        return registro_id

    async def issue_certidao(self, registro_id: UUID, valid: bool = True, referencia: str | None = None) -> None:
        causation = self._last_event.get(str(registro_id))
        evt = CertidaoEmitidaEvent(registro_id=registro_id, certidao_id=uuid4(), referencia=referencia, valid=valid)
        domain_event = evt.to_domain_event(
            aggregate_type="Nascimento",
            aggregate_id=registro_id,
            correlation_id=registro_id,
            causation_id=causation,
        )
        published = await self._publisher.publish_atomic(domain_event, aggregate_id=registro_id, aggregate_type="Nascimento")
        try:
            self._last_event[str(registro_id)] = published.event_id
        except Exception:
            pass

    async def assign_nif(self, registro_id: UUID, nif: str) -> None:
        causation = self._last_event.get(str(registro_id))
        evt = NIFAtribuidoEvent(registro_id=registro_id, nif=nif)
        domain_event = evt.to_domain_event(
            aggregate_type="Nascimento",
            aggregate_id=registro_id,
            correlation_id=registro_id,
            causation_id=causation,
        )
        published = await self._publisher.publish_atomic(domain_event, aggregate_id=registro_id, aggregate_type="Nascimento")
        try:
            self._last_event[str(registro_id)] = published.event_id
        except Exception:
            pass

    async def assign_ss(self, registro_id: UUID, ss_number: str) -> None:
        causation = self._last_event.get(str(registro_id))
        evt = SSAtribuidoEvent(registro_id=registro_id, ss_number=ss_number)
        domain_event = evt.to_domain_event(
            aggregate_type="Nascimento",
            aggregate_id=registro_id,
            correlation_id=registro_id,
            causation_id=causation,
        )
        published = await self._publisher.publish_atomic(domain_event, aggregate_id=registro_id, aggregate_type="Nascimento")
        try:
            self._last_event[str(registro_id)] = published.event_id
        except Exception:
            pass

    async def cancel(self, registro_id: UUID, motivo: str | None = None) -> None:
        causation = self._last_event.get(str(registro_id))
        evt = RegistroCanceladoEvent(registro_id=registro_id, motivo=motivo)
        domain_event = evt.to_domain_event(
            aggregate_type="Nascimento",
            aggregate_id=registro_id,
            correlation_id=registro_id,
            causation_id=causation,
        )
        await self._publisher.publish_atomic(domain_event, aggregate_id=registro_id, aggregate_type="Nascimento")
