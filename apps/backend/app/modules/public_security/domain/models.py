"""
Domain models for public_security module.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(frozen=True)
class PublicSecurityID:
    """Value object for public_security aggregate ID."""

    value: UUID = field(default_factory=uuid4)

    def __str__(self) -> str:
        return str(self.value)


@dataclass
class PublicSecurityAggregate:
    """PublicSecurity aggregate root."""

    id: PublicSecurityID
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if self.id is None:
            object.__setattr__(self, "id", PublicSecurityID())
