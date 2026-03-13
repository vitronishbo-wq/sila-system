from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from apps.backend.app.core.db import AsyncSessionLocal
from apps.backend.app.modules.infrastructure.infrastructure.persistence.saga_model import SagaInstanceModel

class SQLAlchemySagaRepository:

    def __init__(self, *, session_factory: async_sessionmaker[AsyncSession] | None=None) -> None:
        self._session_factory = session_factory or AsyncSessionLocal

    async def get_by_correlation(self, session: AsyncSession, *, saga_type: str, correlation_id: str, tenant_id: str | None=None) -> SagaInstanceModel | None:
        stmt = select(SagaInstanceModel).where(SagaInstanceModel.saga_type == saga_type)
        if tenant_id:
            stmt = stmt.where(SagaInstanceModel.tenant_id == tenant_id)
        stmt = stmt.where(SagaInstanceModel.correlation_id == correlation_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    async def create_if_absent(self, session: AsyncSession, *, saga_type: str, correlation_id: str, tenant_id: str, state: str, data: dict) -> SagaInstanceModel:
        current = await self.get_by_correlation(session, saga_type=saga_type, correlation_id=correlation_id, tenant_id=tenant_id)
        if current is not None:
            return current
        row = SagaInstanceModel(saga_type=saga_type, correlation_id=correlation_id, tenant_id=tenant_id, state=state, data=data)
        try:
            async with session.begin_nested():
                session.add(row)
                await session.flush()
            return row
        except IntegrityError:
            existing = await self.get_by_correlation(session, saga_type=saga_type, correlation_id=correlation_id, tenant_id=tenant_id)
            if existing is not None:
                return existing
            raise

    async def update_state(self, session: AsyncSession, *, row: SagaInstanceModel, state: str, data: dict, completed: bool=False) -> SagaInstanceModel:
        now = datetime.now(timezone.utc)
        row.state = state
        row.data = data
        row.updated_at = now
        row.completed_at = now if completed else row.completed_at
        await session.flush()
        return row
