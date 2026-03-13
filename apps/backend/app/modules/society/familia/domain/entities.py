from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4
from apps.backend.app.modules.society.familia.domain.enums import MemberRole, RelationshipType

def _utcnow() -> datetime:
    return datetime.now(timezone.utc)

@dataclass
class FamilyMember:
    family_id: UUID
    citizen_id: UUID
    role: MemberRole
    joined_at: datetime = field(default_factory=_utcnow)
    left_at: datetime | None = None
    id: UUID = field(default_factory=uuid4)

@dataclass
class FamilyRelationship:
    citizen_a_id: UUID
    citizen_b_id: UUID
    relationship_type: RelationshipType
    start_date: datetime
    end_date: datetime | None = None
    id: UUID = field(default_factory=uuid4)