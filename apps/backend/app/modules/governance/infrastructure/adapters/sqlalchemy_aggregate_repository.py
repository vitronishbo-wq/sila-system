from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.governance.domain.ports.aggregate_repository_port import (
    AggregateRepositoryPort,
)


class SQLAlchemyAggregateRepository(AggregateRepositoryPort):
    """Adapter: Generic SQLAlchemy repository for governance aggregates."""

    def __init__(self, session: AsyncSession, model_class):
        self.session = session
        self.model_class = model_class

    async def create(self, aggregate) -> None:
        """Create a new aggregate."""
        self.session.add(aggregate)
        await self.session.flush()

    async def save(self, aggregate) -> None:
        """Save/update an aggregate."""
        await self.session.merge(aggregate)
        await self.session.flush()

    async def get_by_id(self, id: str) -> object | None:
        """Get aggregate by ID."""
        return await self.session.get(self.model_class, id)

    async def list_all(self, limit: int = 100, offset: int = 0) -> list[object]:
        """List all aggregates."""
        return []

    async def delete(self, id: str) -> bool:
        """Delete an aggregate."""
        aggregate = await self.get_by_id(id)
        if aggregate:
            await self.session.delete(aggregate)
            await self.session.flush()
            return True
        return False
