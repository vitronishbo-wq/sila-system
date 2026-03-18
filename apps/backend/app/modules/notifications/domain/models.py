"""
Domain models for notifications module.
"""
from __future__ import annotations
from uuid import UUID, uuid4
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

@dataclass(frozen=True)
class NotificationsID:
    """Value object for notifications aggregate ID."""
    value: UUID = field(default_factory=uuid4)

    def __str__(self) -> str:
        return str(self.value)

@dataclass
class NotificationsAggregate:
    """Notifications aggregate root."""
    id: NotificationsID
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if self.id is None:
            object.__setattr__(self, 'id', NotificationsID())