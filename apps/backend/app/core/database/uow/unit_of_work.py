from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork:
    """Async unit of work that commits or rolls back a shared session."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self) -> UnitOfWork:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> bool:
        if exc_type:
            await self.session.rollback()
            return False
        await self.session.commit()
        return False
