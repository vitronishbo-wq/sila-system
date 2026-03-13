import uuid
from typing import Any, Dict
from sqlalchemy.orm import Session
from .models import CitizenEventModel, EventType
from apps.backend.app.modules.justice.bounded_contexts.projections.projectors import CitizenProjector

def register_event(db: Session, citizen_id: uuid.UUID, event_type: EventType, payload: Dict[str, Any], legal_basis: str, service_id: str, performed_by: str) -> CitizenEventModel:
    if isinstance(event_type, str):
        try:
            event_type = EventType(event_type)
        except ValueError:
            raise ValueError(f"Tipo de evento '{event_type}' não é reconhecido pelo sistema SILA.")
    new_event = CitizenEventModel(citizen_id=citizen_id, event_type=event_type, payload=payload, legal_basis=legal_basis, service_id=service_id, performed_by=performed_by)
    try:
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        projector = CitizenProjector(db)
        projector.apply_event(new_event)
        return new_event
    except Exception as e:
        db.rollback()
        raise RuntimeError(f'Falha crítica ao gravar na memória jurídica do Estado: {str(e)}')