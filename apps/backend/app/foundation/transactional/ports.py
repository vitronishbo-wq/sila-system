from __future__ import annotations

from typing import Protocol
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession


class TransferTransactionalPort(Protocol):
    async def execute_transfer(self, session: AsyncSession, payload: dict, idempotency_key: str) -> dict:
        """Execute a transfer pipeline inside the provided session and return a canonical receipt."""


class EnrollmentStateMachinePort(Protocol):
    async def transition(self, session: AsyncSession, enrollment_id: UUID, event: str, actor_id: UUID) -> dict:
        """Apply a state transition to an enrollment atomically and return resulting state snapshot."""


class CapacityReservationPort(Protocol):
    async def reserve(self, session: AsyncSession, institution_id: UUID, grade: str, shift: str, quantity: int = 1, for_update: bool = True) -> dict | None:
        """Reserve capacity for an institution/grade/shift. Returns reservation metadata including `id`."""

    async def release(self, session: AsyncSession, id: UUID, quantity: int = 1) -> dict | None:
        """Release a prior reservation by capacity record id."""

    async def get_available(self, session: AsyncSession, institution_id: UUID, grade: str, shift: str) -> int:
        """Return currently available seats for the institution/grade/shift."""

