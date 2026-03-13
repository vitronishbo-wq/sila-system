from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class FamilyHeadTransferredEvent:
    aggregate_id: UUID
    old_head_citizen_id: UUID
    new_head_citizen_id: UUID
    occurred_at: datetime
    event_name: str = 'FamilyHeadTransferred'

    def to_payload(self) -> dict:
        return {'aggregate_id': str(self.aggregate_id), 'old_head_citizen_id': str(self.old_head_citizen_id), 'new_head_citizen_id': str(self.new_head_citizen_id), 'occurred_at': self.occurred_at.isoformat()}