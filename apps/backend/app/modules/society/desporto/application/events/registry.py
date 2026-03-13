from __future__ import annotations
from dataclasses import asdict, is_dataclass
from typing import Any
from apps.backend.app.modules.society.desporto.application.events.definitions import ContratoAssinadoEvent, DomainEvent, EstadioCadastradoEvent, JogoAgendadoEvent, JogoResultadoRegistradoEvent, TransferenciaConcluidaEvent, TransferenciaSolicitadaEvent
EVENT_REGISTRY: dict[str, type[DomainEvent]] = {'JogoAgendadoEvent': JogoAgendadoEvent, 'JogoResultadoRegistradoEvent': JogoResultadoRegistradoEvent, 'EstadioCadastradoEvent': EstadioCadastradoEvent, 'TransferenciaSolicitadaEvent': TransferenciaSolicitadaEvent, 'TransferenciaConcluidaEvent': TransferenciaConcluidaEvent, 'ContratoAssinadoEvent': ContratoAssinadoEvent}

def serialize_event(event: object) -> tuple[str, dict[str, Any]]:
    event_name = type(event).__name__
    if hasattr(event, 'to_payload') and callable(event.to_payload):
        payload = dict(event.to_payload())
    elif is_dataclass(event):
        payload = asdict(event)
    else:
        payload = {'repr': repr(event)}
    return (event_name, payload)

def deserialize_event(event_name: str, payload: dict[str, Any]) -> object:
    event_cls = EVENT_REGISTRY.get(event_name)
    if event_cls is None:
        return {'event_name': event_name, 'payload': payload}
    try:
        return event_cls(**payload)
    except Exception:
        return {'event_name': event_name, 'payload': payload}