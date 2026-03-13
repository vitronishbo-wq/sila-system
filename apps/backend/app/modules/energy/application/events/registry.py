from __future__ import annotations
from typing import Any
from apps.backend.app.modules.energy.application.events.definitions import DemandaCriticaEvent, FaturaGeradaEvent, InterrupcaoEvent, LeituraRealizadaEvent, QualidadeInconformeEvent

class EnergiaEventRegistry:
    PUBLISHABLE_EVENTS = {LeituraRealizadaEvent.event_name: 'energia.leitura.realizada', FaturaGeradaEvent.event_name: 'energia.fatura.gerada', InterrupcaoEvent.event_name: 'energia.interrupcao', QualidadeInconformeEvent.event_name: 'energia.qualidade.inconforme', DemandaCriticaEvent.event_name: 'energia.demanda.critica'}
    _DESERIALIZERS = {LeituraRealizadaEvent.event_name: LeituraRealizadaEvent.from_payload, FaturaGeradaEvent.event_name: FaturaGeradaEvent.from_payload, InterrupcaoEvent.event_name: InterrupcaoEvent.from_payload, QualidadeInconformeEvent.event_name: QualidadeInconformeEvent.from_payload, DemandaCriticaEvent.event_name: DemandaCriticaEvent.from_payload}

def serialize_event(event: Any) -> tuple[str, dict]:
    if not hasattr(event, 'event_name') or not hasattr(event, 'to_payload'):
        raise ValueError('Evento invalido para serializacao')
    return (event.event_name, event.to_payload())

def deserialize_event(event_name: str, payload: dict) -> Any:
    factory = EnergiaEventRegistry._DESERIALIZERS.get(event_name)
    if factory is None:
        raise ValueError(f'Evento nao suportado: {event_name}')
    return factory(payload)
