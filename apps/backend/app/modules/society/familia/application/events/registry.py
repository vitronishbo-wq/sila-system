from __future__ import annotations
from uuid import UUID
from app.modules.society.familia.application.events.definitions import DomainEvent

def deserialize_event(event_name: str, payload: dict) -> DomainEvent:
    aggregate_id = payload.get('aggregate_id') or payload.get('id')
    if aggregate_id is None:
        raise ValueError(f'Payload invalido para evento {event_name}')
    return DomainEvent(aggregate_id=UUID(str(aggregate_id)), event_name=event_name, payload=payload)