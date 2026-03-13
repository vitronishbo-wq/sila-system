from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class FamilyMemberRemovedEvent:
    aggregate_id: UUID
    citizen_id: UUID
    occurred_at: datetime
    reason: str | None = None
    event_name: str = 'FamilyMemberRemoved'

    def to_payload(self) -> dict:
        return {'aggregate_id': str(self.aggregate_id), 'citizen_id': str(self.citizen_id), 'reason': self.reason, 'occurred_at': self.occurred_at.isoformat()}