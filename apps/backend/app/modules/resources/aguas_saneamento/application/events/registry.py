from __future__ import annotations
from typing import Any
from apps.backend.app.modules.resources.aguas_saneamento.application.events.fatura_events import FaturaEmitidaEvent, FaturaPagamentoRegistradoEvent

class AguasEventRegistry:
    PUBLISHABLE_EVENTS = {FaturaEmitidaEvent.event_name: 'aguas.fatura.emitida', FaturaPagamentoRegistradoEvent.event_name: 'aguas.fatura.pagamento_registrado'}
    _DESERIALIZERS = {FaturaEmitidaEvent.event_name: FaturaEmitidaEvent.from_payload, FaturaPagamentoRegistradoEvent.event_name: FaturaPagamentoRegistradoEvent.from_payload}

def serialize_event(event: Any) -> tuple[str, dict]:
    if not hasattr(event, 'event_name') or not hasattr(event, 'to_payload'):
        raise ValueError('Evento invalido para serializacao')
    return (event.event_name, event.to_payload())

def deserialize_event(event_name: str, payload: dict) -> Any:
    factory = AguasEventRegistry._DESERIALIZERS.get(event_name)
    if factory is None:
        raise ValueError(f'Evento nao suportado: {event_name}')
    return factory(payload)