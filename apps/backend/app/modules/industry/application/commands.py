"""
Application commands for industry module.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateIndustryCommand:
    """Command to create a new industry."""

    id: UUID | None = None

    def __post_init__(self):
        if not self.id:
            from uuid import uuid4

            object.__setattr__(self, "id", uuid4())


@dataclass
class UpdateIndustryCommand:
    """Command to update a industry."""

    id: UUID

    def validate(self) -> None:
        if not self.id:
            raise ValueError("ID required for update")


@dataclass
class DeleteIndustryCommand:
    """Command to delete a industry."""

    id: UUID
