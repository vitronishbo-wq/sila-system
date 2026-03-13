from __future__ import annotations
from typing import Any
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.events.definitions import FaturaTelecomGeradaEvent, QualidadeServicoAferidaEvent, ReclamacaoTelecomAbertaEvent

class TelecomEventRegistry:
    PUBLISHABLE_EVENTS = {FaturaTelecomGeradaEvent.event_name: 'telecom.fatura.gerada', ReclamacaoTelecomAbertaEvent.event_name: 'telecom.reclamacao.aberta', QualidadeServicoAferidaEvent.event_name: 'telecom.qualidade.aferida'}
    _DESERIALIZERS = {FaturaTelecomGeradaEvent.event_name: FaturaTelecomGeradaEvent.from_payload, ReclamacaoTelecomAbertaEvent.event_name: ReclamacaoTelecomAbertaEvent.from_payload, QualidadeServicoAferidaEvent.event_name: QualidadeServicoAferidaEvent.from_payload}

def serialize_event(event: Any) -> tuple[str, dict]:
    if not hasattr(event, 'event_name') or not hasattr(event, 'to_payload'):
        raise ValueError('Evento invalido para serializacao')
    return (event.event_name, event.to_payload())

def deserialize_event(event_name: str, payload: dict) -> Any:
    factory = TelecomEventRegistry._DESERIALIZERS.get(event_name)
    if factory is None:
        raise ValueError(f'Evento nao suportado: {event_name}')
    return factory(payload)