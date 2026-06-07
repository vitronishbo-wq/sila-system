"""
Application commands for documents module.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateDocumentsCommand:
    """Command to create a new documents."""

    id: UUID | None = None

    def __post_init__(self):
        if not self.id:
            from uuid import uuid4

            object.__setattr__(self, "id", uuid4())


@dataclass
class UpdateDocumentsCommand:
    """Command to update a documents."""

    id: UUID

    def validate(self) -> None:
        if not self.id:
            raise ValueError("ID required for update")


@dataclass
class DeleteDocumentsCommand:
    """Command to delete a documents."""

    id: UUID
