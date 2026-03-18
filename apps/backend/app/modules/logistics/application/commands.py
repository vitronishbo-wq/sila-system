"""
Application commands for logistics module.
"""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

@dataclass
class CreateLogisticsCommand:
    """Command to create a new logistics."""
    id: Optional[UUID] = None

    def __post_init__(self):
        if not self.id:
            from uuid import uuid4
            object.__setattr__(self, 'id', uuid4())

@dataclass
class UpdateLogisticsCommand:
    """Command to update a logistics."""
    id: UUID

    def validate(self) -> None:
        if not self.id:
            raise ValueError('ID required for update')

@dataclass
class DeleteLogisticsCommand:
    """Command to delete a logistics."""
    id: UUID