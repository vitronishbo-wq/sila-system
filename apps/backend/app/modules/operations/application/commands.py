"""
Application commands for operations module.
"""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

@dataclass
class CreateOperationsCommand:
    """Command to create a new operations."""
    id: Optional[UUID] = None

    def __post_init__(self):
        if not self.id:
            from uuid import uuid4
            object.__setattr__(self, 'id', uuid4())

@dataclass
class UpdateOperationsCommand:
    """Command to update a operations."""
    id: UUID

    def validate(self) -> None:
        if not self.id:
            raise ValueError('ID required for update')

@dataclass
class DeleteOperationsCommand:
    """Command to delete a operations."""
    id: UUID