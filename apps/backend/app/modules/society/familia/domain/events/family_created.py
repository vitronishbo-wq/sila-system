from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class FamilyCreatedEvent:
    aggregate_id: UUID
    head_citizen_id: UUID
    code: str
    occurred_at: datetime
    event_name: str = 'FamilyCreated'

    def to_payload(self) -> dict:
        return {'aggregate_id': str(self.aggregate_id), 'head_citizen_id': str(self.head_citizen_id), 'code': self.code, 'occurred_at': self.occurred_at.isoformat()}