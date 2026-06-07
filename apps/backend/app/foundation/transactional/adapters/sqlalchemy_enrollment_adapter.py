from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.foundation.transactional.ports import EnrollmentStateMachinePort
from apps.backend.app.modules.educacao.infrastructure.repositories.sqlalchemy_enrollment_repository import (
    SQLAlchemyEnrollmentRepository,
)


class SQLAlchemyEnrollmentStateMachineAdapter(EnrollmentStateMachinePort):
    """Adapter that implements EnrollmentStateMachinePort using the existing enrollment repository.

    This adapter keeps transitions simple and delegates to `update_status` on the repository.
    Applications can implement richer semantics (history, outbox emission, audit) by composing
    this adapter with other adapters (outbox, audit) inside higher-level orchestration.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = SQLAlchemyEnrollmentRepository(session)

    async def transition(self, session: AsyncSession, enrollment_id: UUID, event: str, actor_id: UUID) -> dict | None:
        # Simple event → status mapping
        mapping = {
            "activate": "ACTIVE",
            "pending": "PENDING",
            "transfer": "TRANSFERRED",
            "complete": "COMPLETED",
        }
        status = mapping.get(event)
        if not status:
            raise ValueError(f"Unknown enrollment event: {event}")
        return await self.repo.update_status(enrollment_id, status)
