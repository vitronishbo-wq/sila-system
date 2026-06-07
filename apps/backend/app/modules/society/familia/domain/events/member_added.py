from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from apps.backend.app.modules.society.familia.domain.enums import MemberRole


@dataclass(frozen=True)
class FamilyMemberAddedEvent:
    aggregate_id: UUID
    citizen_id: UUID
    role: MemberRole
    occurred_at: datetime
    event_name: str = "FamilyMemberAdded"

    def to_payload(self) -> dict:
        return {
            "aggregate_id": str(self.aggregate_id),
            "citizen_id": str(self.citizen_id),
            "role": self.role.value,
            "occurred_at": self.occurred_at.isoformat(),
        }
