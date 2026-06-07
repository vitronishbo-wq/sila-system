from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


def _utcnow() -> datetime:
    return datetime.now(UTC)


@dataclass(frozen=True)
class DomainEvent:
    aggregate_id: UUID
    event_name: str
    payload: dict
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=_utcnow)
    version: int = 1

    def to_payload(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "aggregate_id": str(self.aggregate_id),
            "event_name": self.event_name,
            "occurred_at": self.occurred_at.isoformat(),
            "version": self.version,
            "payload": self.payload,
        }
