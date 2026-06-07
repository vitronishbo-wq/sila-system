from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(kw_only=True)
class CulturalEvent:
    event_id: UUID = field(default_factory=uuid4)
    asset_id: UUID
    name: str
    event_date: datetime
    organizer: str
    description: str | None = None
    expected_attendance: int | None = None
    requires_authorization: bool = False
    authorization_status: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def authorize(self, authorized_by: str) -> None:
        if self.requires_authorization:
            self.authorization_status = f"AUTHORIZED_BY_{authorized_by}"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "asset_id": str(self.asset_id),
            "name": self.name,
            "event_date": self.event_date.isoformat(),
            "organizer": self.organizer,
            "description": self.description,
            "expected_attendance": self.expected_attendance,
            "requires_authorization": self.requires_authorization,
            "authorization_status": self.authorization_status,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> CulturalEvent:
        return cls(
            event_id=UUID(data["event_id"]),
            asset_id=UUID(data["asset_id"]),
            name=data["name"],
            event_date=datetime.fromisoformat(data["event_date"]),
            organizer=data["organizer"],
            description=data.get("description"),
            expected_attendance=data.get("expected_attendance"),
            requires_authorization=data.get("requires_authorization", False),
            authorization_status=data.get("authorization_status"),
            created_at=datetime.fromisoformat(data["created_at"]),
        )
