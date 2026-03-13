from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

@dataclass(frozen=True)
class DomainEvent:
    """Base event contract for in-process domain events."""
    event_id: UUID = field(default_factory=uuid4)
    event_type: str = 'domain.event'
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    payload: dict[str, Any] = field(default_factory=dict)