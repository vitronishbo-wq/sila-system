"""
Application commands for procurement module.
"""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

@dataclass
class CreateProcurementCommand:
    """Command to create a new procurement."""
    id: Optional[UUID] = None

    def __post_init__(self):
        if not self.id:
            from uuid import uuid4
            object.__setattr__(self, 'id', uuid4())

@dataclass
class UpdateProcurementCommand:
    """Command to update a procurement."""
    id: UUID

    def validate(self) -> None:
        if not self.id:
            raise ValueError('ID required for update')

@dataclass
class DeleteProcurementCommand:
    """Command to delete a procurement."""
    id: UUID