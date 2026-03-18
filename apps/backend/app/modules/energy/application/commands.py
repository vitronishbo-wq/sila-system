"""
Application commands for energy module.
"""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

@dataclass
class CreateEnergyCommand:
    """Command to create a new energy."""
    id: Optional[UUID] = None

    def __post_init__(self):
        if not self.id:
            from uuid import uuid4
            object.__setattr__(self, 'id', uuid4())

@dataclass
class UpdateEnergyCommand:
    """Command to update a energy."""
    id: UUID

    def validate(self) -> None:
        if not self.id:
            raise ValueError('ID required for update')

@dataclass
class DeleteEnergyCommand:
    """Command to delete a energy."""
    id: UUID