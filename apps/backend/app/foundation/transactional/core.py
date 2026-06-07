from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from .ports import CapacityReservationPort, EnrollmentStateMachinePort, TransferTransactionalPort


class TransferTransactionalEngine(TransferTransactionalPort):
    """Skeleton implementation for Transfer transactional orchestration.

    This class coordinates locks, capacity reservation, enrollment state transitions,
    outbox persistence and audit inside a single Unit-of-Work (provided AsyncSession).
    Concrete adapters (repositories, outbox, audit) must be injected by the application module.
    """

    def __init__(self, *, capacity: CapacityReservationPort, enrollment_sm: EnrollmentStateMachinePort, **adapters: Any):
        self.capacity = capacity
        self.enrollment_sm = enrollment_sm
        self.adapters = adapters

    async def execute_transfer(self, session: AsyncSession, payload: dict, idempotency_key: str) -> dict:
        """High-level orchestration. Implementation TODO: implement orchestration steps.

        Keep this method small: acquire locks in canonical order, call adapters, persist outbox, then return receipt.
        """
        # Minimal orchestration implementation for integration:
        # - payload must contain: institution_id, grade, shift, current_enrollment_id, actor_id
        institution_id = payload.get("institution_id")
        grade = payload.get("grade")
        shift = payload.get("shift")
        current_enrollment_id = payload.get("current_enrollment_id")
        actor_id = payload.get("actor_id")

        if not all([institution_id, grade, shift, current_enrollment_id]):
            raise ValueError("Missing transfer payload fields")

        # 1) Reserve capacity
        reservation = await self.capacity.reserve(session, institution_id, grade, shift, quantity=1)
        if reservation is None:
            raise ValueError("No capacity available")

        # 2) Transition enrollment to TRANSFERRED (and expect adapter to create new enrollment)
        enrollment_after = await self.enrollment_sm.transition(session, current_enrollment_id, "transfer", actor_id)

        # 3) Build a canonical receipt
        from uuid import uuid4
        receipt = {
            "transfer_id": str(uuid4()),
            "status": "success",
            "reservation": reservation,
            "enrollment_after": enrollment_after,
        }
        return receipt


class EnrollmentStateMachine:
    """Skeleton for enrollment state machine helper.

    This is a convenience engine; prefer implementing the external Port interface.
    """

    async def transition(self, session: AsyncSession, enrollment_id: UUID, event: str, actor_id: UUID) -> dict:
        raise NotImplementedError()


class CapacityReservationEngine:
    """Skeleton engine that should wrap existing capacity repository logic and provide TTL/lease support."""

    async def reserve(self, session: AsyncSession, turma_id: UUID, qty: int = 1, for_update: bool = True) -> dict:
        raise NotImplementedError()

    async def release(self, session: AsyncSession, reservation_id: UUID) -> None:
        raise NotImplementedError()

    async def get_available(self, session: AsyncSession, turma_id: UUID) -> int:
        raise NotImplementedError()

