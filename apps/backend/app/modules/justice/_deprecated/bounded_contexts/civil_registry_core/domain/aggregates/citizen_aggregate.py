from __future__ import annotations
from datetime import date, datetime
from uuid import uuid4
from apps.backend.app.core.events.base_event import BaseEvent
from apps.backend.app.core.observability.context import get_request_id
from ..models.citizen import Citizen
from ..models.bi_record import BIRecord

class DomainException(Exception):
    pass

class DuplicateBIRecord(DomainException):
    pass

class CitizenRegisteredEvent(BaseEvent):
    event_type = 'CITIZEN_REGISTERED'

class CitizenAggregate:

    def __init__(self, citizen_id: str | None=None):
        self.id = citizen_id or str(uuid4())
        self.citizen: Citizen | None = None
        self.bi_record: BIRecord | None = None
        self.events: list[BaseEvent] = []

    def register_birth(self, data: dict, bi_number: str) -> None:
        if not bi_number:
            raise DomainException('BI obrigatório')
        full_name = data.get('name') or data.get('full_name')
        if not full_name:
            raise DomainException('Nome obrigatório')
        birth_date = data.get('birth_date') or data.get('date_of_birth')
        if isinstance(birth_date, str):
            try:
                birth_date = date.fromisoformat(birth_date)
            except Exception:
                birth_date = None
        self.citizen = Citizen(citizen_id=self.id, full_name=full_name, birth_date=birth_date, created_at=datetime.utcnow())
        self.bi_record = BIRecord(citizen_fuc_id=self.id, bi_number=bi_number, issue_date=date.today(), expiry_date=None, status='active')
        event = CitizenRegisteredEvent(aggregate_id=self.id, payload=data, metadata={'request_id': get_request_id()})
        self.events.append(event)

    @classmethod
    def create_citizen(cls, data: dict, bi_number: str, citizen_id: str | None=None) -> 'CitizenAggregate':
        agg = cls(citizen_id=citizen_id)
        agg.register_birth(data, bi_number)
        return agg