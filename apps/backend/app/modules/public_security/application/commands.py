"""
Application commands for public_security module.
"""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

@dataclass
class CreatePublicSecurityCommand:
    """Command to create a new public_security."""
    id: Optional[UUID] = None

    def __post_init__(self):
        if not self.id:
            from uuid import uuid4
            object.__setattr__(self, 'id', uuid4())

@dataclass
class UpdatePublicSecurityCommand:
    """Command to update a public_security."""
    id: UUID

    def validate(self) -> None:
        if not self.id:
            raise ValueError('ID required for update')

@dataclass
class DeletePublicSecurityCommand:
    """Command to delete a public_security."""
    id: UUID