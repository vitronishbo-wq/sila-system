from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.bridges.identity_bridge import CitizenFUC
from apps.backend.app.modules.justice.bounded_contexts.infrastructure.models.citizen_event_model import CitizenEventModel, EventType

class CitizenProjector:

    def __init__(self, db: Session, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.db = db

    def apply_event(self, event: CitizenEventModel):
        """Apply event to citizen projection."""
        handler_map = {EventType.BIRTH_REGISTRATION: self._handle_birth, EventType.ADDRESS_UPDATE: self._handle_address_update, EventType.VITAL_STATUS_CHANGE: self._handle_vital_status_change, EventType.ID_CARD_ISSUED: self._handle_id_card}
        handler = handler_map.get(event.event_type)
        if handler:
            handler(event)
            self.db.commit()

    def _handle_birth(self, event: CitizenEventModel):
        """Handle BIRTH_REGISTRATION event."""
        payload = event.payload
        result = self.db.execute(select(CitizenFUC).where(CitizenFUC.citizen_id == event.citizen_id))
        projection = result.scalar_one_or_none()
        if projection:
            projection.full_name = payload.get('full_name', projection.full_name)
            projection.birth_date = payload.get('birth_date')
            projection.gender = payload.get('gender', 'O')
            projection.nationality = payload.get('nationality')
        else:
            projection = CitizenFUC(citizen_id=event.citizen_id, full_name=payload.get('full_name'), birth_date=payload.get('birth_date'), gender=payload.get('gender', 'O'), nationality=payload.get('nationality'), vital_status='ALIVE', version=1, last_event_id=event.id)
            self.db.add(projection)
        if not projection.history:
            projection.history = []
        projection.history.append({'type': event.event_type.value, 'id': str(event.id), 'timestamp': datetime.utcnow().isoformat(), 'payload': payload})
        projection.last_event_id = event.id
        projection.version = (projection.version or 0) + 1
        projection.updated_at = datetime.utcnow()

    def _handle_address_update(self, event: CitizenEventModel):
        """Handle ADDRESS_UPDATE event."""
        result = self.db.execute(select(CitizenFUC).where(CitizenFUC.citizen_id == event.citizen_id))
        projection = result.scalar_one_or_none()
        if projection:
            payload = event.payload
            projection.current_address = payload.get('residence') or payload.get('new_address')
            projection.province_id = payload.get('province_id')
            projection.municipality_id = payload.get('municipality_id')
            projection.commune_id = payload.get('commune_id')
            projection.last_event_id = event.id
            projection.version = (projection.version or 0) + 1
            if not projection.history:
                projection.history = []
            projection.history.append({'type': event.event_type.value, 'id': str(event.id), 'timestamp': datetime.utcnow().isoformat(), 'payload': event.payload})
            projection.updated_at = datetime.utcnow()

    def _handle_vital_status_change(self, event: CitizenEventModel):
        """Handle VITAL_STATUS_CHANGE event."""
        result = self.db.execute(select(CitizenFUC).where(CitizenFUC.citizen_id == event.citizen_id))
        projection = result.scalar_one_or_none()
        if projection:
            new_status = event.payload.get('status', 'ALIVE').upper()
            if new_status in ['ALIVE', 'DECEASED', 'UNKNOWN']:
                projection.vital_status = new_status
            projection.last_event_id = event.id
            projection.version = (projection.version or 0) + 1
            if not projection.history:
                projection.history = []
            projection.history.append({'type': event.event_type.value, 'id': str(event.id), 'timestamp': datetime.utcnow().isoformat(), 'payload': event.payload})
            projection.updated_at = datetime.utcnow()

    def _handle_id_card(self, event: CitizenEventModel):
        """Handle ID_CARD_ISSUED event."""
        result = self.db.execute(select(CitizenFUC).where(CitizenFUC.citizen_id == event.citizen_id))
        projection = result.scalar_one_or_none()
        if projection:
            payload = event.payload
            projection.id_number = payload.get('card_id')
            projection.document_number = payload.get('card_id')
            projection.nif = payload.get('nif')
            projection.last_event_id = event.id
            projection.version = (projection.version or 0) + 1
            if not projection.history:
                projection.history = []
            projection.history.append({'type': event.event_type.value, 'id': str(event.id), 'timestamp': datetime.utcnow().isoformat(), 'payload': event.payload})
            projection.updated_at = datetime.utcnow()
__all__ = ['CitizenProjector']