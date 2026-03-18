"""
Application commands for infrastructure_sector module.
"""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

@dataclass
class CreateInfrastructureSectorCommand:
    """Command to create a new infrastructure_sector."""
    id: Optional[UUID] = None

    def __post_init__(self):
        if not self.id:
            from uuid import uuid4
            object.__setattr__(self, 'id', uuid4())

@dataclass
class UpdateInfrastructureSectorCommand:
    """Command to update a infrastructure_sector."""
    id: UUID

    def validate(self) -> None:
        if not self.id:
            raise ValueError('ID required for update')

@dataclass
class DeleteInfrastructureSectorCommand:
    """Command to delete a infrastructure_sector."""
    id: UUID