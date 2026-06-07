from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.foundation.transactional.ports import CapacityReservationPort
from apps.backend.app.modules.educacao.infrastructure.repositories.sqlalchemy_capacity_repository import (
    SQLAlchemyCapacityRepository,
)


class SQLAlchemyCapacityReservationAdapter(CapacityReservationPort):
    """Adapter that wraps existing `SQLAlchemyCapacityRepository` to satisfy the `CapacityReservationPort`.

    Note: this adapter forwards calls to the concrete repository. The repository must be constructed
    with the same `AsyncSession` passed to adapter methods (or the adapter can accept a session
    per-method and instantiate the repository each call).
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = SQLAlchemyCapacityRepository(session)

    async def reserve(self, session: AsyncSession, institution_id: UUID, grade: str, shift: str, quantity: int = 1, for_update: bool = True) -> dict | None:
        """Reserve capacity by delegating to `reserve_capacity`.

        Compatibility note: the underlying repository expects `(institution_id, grade, shift, quantity)`.
        """
        # delegate to repository
        return await self.repo.reserve_capacity(institution_id, grade, shift, quantity)

    async def release(self, session: AsyncSession, id: UUID, quantity: int = 1) -> dict | None:
        return await self.repo.release_capacity(id, quantity)

    async def get_available(self, session: AsyncSession, institution_id: UUID, grade: str, shift: str) -> int:
        return await self.repo.get_available(institution_id, grade, shift)
