"""
Application commands for payment module.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreatePaymentCommand:
    """Command to create a new payment."""

    id: UUID | None = None

    def __post_init__(self):
        if not self.id:
            from uuid import uuid4

            object.__setattr__(self, "id", uuid4())


@dataclass
class UpdatePaymentCommand:
    """Command to update a payment."""

    id: UUID

    def validate(self) -> None:
        if not self.id:
            raise ValueError("ID required for update")


@dataclass
class DeletePaymentCommand:
    """Command to delete a payment."""

    id: UUID
