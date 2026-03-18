"""
Domain models for infrastructure_sector module.
"""
from __future__ import annotations
from uuid import UUID, uuid4
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

@dataclass(frozen=True)
class InfrastructureSectorID:
    """Value object for infrastructure_sector aggregate ID."""
    value: UUID = field(default_factory=uuid4)

    def __str__(self) -> str:
        return str(self.value)

@dataclass
class InfrastructureSectorAggregate:
    """InfrastructureSector aggregate root."""
    id: InfrastructureSectorID
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if self.id is None:
            object.__setattr__(self, 'id', InfrastructureSectorID())