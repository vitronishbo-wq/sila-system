from __future__ import annotations
from typing import Any, Iterable
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class BaseRepository:
    """Async base repository with simple CRUD helpers (no implicit commits)."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, entity: Any) -> None:
        self.session.add(entity)

    async def add_all(self, entities: Iterable[Any]) -> None:
        self.session.add_all(list(entities))

    async def get(self, model: Any, entity_id: Any) -> Any | None:
        return await self.session.get(model, entity_id)

    async def delete(self, entity: Any) -> None:
        await self.session.delete(entity)

    async def list(self, model: Any, limit: int=100, offset: int=0) -> list[Any]:
        result = await self.session.execute(select(model).limit(limit).offset(offset))
        return list(result.scalars().all())