"""
Domain models for educacao module.
"""
from __future__ import annotations
from uuid import UUID, uuid4
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

@dataclass(frozen=True)
class EducacaoID:
    """Value object for educacao aggregate ID."""
    value: UUID = field(default_factory=uuid4)

    def __str__(self) -> str:
        return str(self.value)

@dataclass
class EducacaoAggregate:
    """Educacao aggregate root."""
    id: EducacaoID
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if self.id is None:
            object.__setattr__(self, 'id', EducacaoID())