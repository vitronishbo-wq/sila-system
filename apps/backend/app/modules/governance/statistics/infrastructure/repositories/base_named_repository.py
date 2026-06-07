from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyNamedRepository:
    def __init__(self, session: AsyncSession, model_cls: type):
        self.session = session
        self.model_cls = model_cls

    async def create(self, data: dict[str, Any]) -> Any:
        model = self.model_cls(**data)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def get_by_id(self, entity_id: int) -> Any | None:
        return await self.session.get(self.model_cls, entity_id)

    async def list_all(self, limit: int = 100, offset: int = 0) -> list[Any]:
        stmt = select(self.model_cls).order_by(self.model_cls.id.asc()).offset(offset).limit(limit)
        return list((await self.session.execute(stmt)).scalars().all())

    async def update(self, entity_id: int, data: dict[str, Any]) -> Any | None:
        model = await self.get_by_id(entity_id)
        if model is None:
            return None
        for key, value in data.items():
            if hasattr(model, key) and value is not None:
                setattr(model, key, value)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def delete(self, entity_id: int) -> bool:
        model = await self.get_by_id(entity_id)
        if model is None:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True
