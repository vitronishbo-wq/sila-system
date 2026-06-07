"""
Application commands for resources module.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateResourcesCommand:
    """Command to create a new resources."""

    id: UUID | None = None

    def __post_init__(self):
        if not self.id:
            from uuid import uuid4

            object.__setattr__(self, "id", uuid4())


@dataclass
class UpdateResourcesCommand:
    """Command to update a resources."""

    id: UUID

    def validate(self) -> None:
        if not self.id:
            raise ValueError("ID required for update")


@dataclass
class DeleteResourcesCommand:
    """Command to delete a resources."""

    id: UUID
