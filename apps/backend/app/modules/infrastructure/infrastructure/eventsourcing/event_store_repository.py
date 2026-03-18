from __future__ import annotations
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from apps.backend.app.core.db import AsyncSessionLocal
from apps.backend.app.modules.infrastructure.infrastructure.eventsourcing.event_store_model import EventStoreModel

class EventStoreConcurrencyError(RuntimeError):
    pass

@dataclass(frozen=True)
class EventStoreEntry:
    id: UUID
    aggregate_id: str
    aggregate_type: str
    event_type: str
    event_data: dict[str, Any]
    version: int
    tenant_id: str
    region_code: str
    correlation_id: str
    created_at: datetime

class SQLAlchemyEventStoreRepository:

    def __init__(self, *, session: AsyncSession | None=None, session_factory: async_sessionmaker[AsyncSession] | None=None, region_code: str | None=None) -> None:
        self._session = session
        self._session_factory = session_factory or AsyncSessionLocal
        self._region_code = (region_code or os.environ.get('OP_REGION_CODE') or 'A').strip().upper()

    async def append_event(self, *, aggregate_id: str, aggregate_type: str, event_type: str, event_data: dict[str, Any], tenant_id: str, correlation_id: str, expected_version: int | None=None) -> EventStoreEntry:
        if not aggregate_id.strip():
            raise ValueError('aggregate_id obrigatorio')
        if expected_version is not None and expected_version < 0:
            raise ValueError('expected_version deve ser >= 0')
        if self._session is not None:
            return await self._append_with_session(self._session, aggregate_id=aggregate_id, aggregate_type=aggregate_type, event_type=event_type, event_data=event_data, tenant_id=tenant_id, correlation_id=correlation_id, expected_version=expected_version)
        async with self._session_factory() as session:
            async with session.begin():
                return await self._append_with_session(session, aggregate_id=aggregate_id, aggregate_type=aggregate_type, event_type=event_type, event_data=event_data, tenant_id=tenant_id, correlation_id=correlation_id, expected_version=expected_version)

    async def list_events(self, session: AsyncSession, *, aggregate_id: str, tenant_id: str | None=None) -> list[EventStoreEntry]:
        stmt = select(EventStoreModel).where(EventStoreModel.aggregate_id == aggregate_id)
        if tenant_id:
            stmt = stmt.where(EventStoreModel.tenant_id == tenant_id)
        stmt = stmt.order_by(EventStoreModel.version.asc())
        result = await session.execute(stmt)
        rows = result.scalars().all()
        return [self._to_entry(row) for row in rows]

    async def list_events_for_aggregate(self, *, aggregate_id: str, tenant_id: str | None=None) -> list[EventStoreEntry]:
        if self._session is not None:
            return await self.list_events(self._session, aggregate_id=aggregate_id, tenant_id=tenant_id)
        async with self._session_factory() as session:
            return await self.list_events(session, aggregate_id=aggregate_id, tenant_id=tenant_id)

    async def get_last_version(self, session: AsyncSession, *, aggregate_id: str, tenant_id: str) -> int:
        stmt = select(func.max(EventStoreModel.version)).where(EventStoreModel.aggregate_id == aggregate_id, EventStoreModel.tenant_id == tenant_id)
        result = await session.execute(stmt)
        return int(result.scalar() or 0)

    async def _append_with_session(self, session: AsyncSession, *, aggregate_id: str, aggregate_type: str, event_type: str, event_data: dict[str, Any], tenant_id: str, correlation_id: str, expected_version: int | None) -> EventStoreEntry:
        current_version = await self.get_last_version(session, aggregate_id=aggregate_id, tenant_id=tenant_id)
        strict_expected = current_version if expected_version is None else expected_version
        if current_version != strict_expected:
            raise EventStoreConcurrencyError(f'Concurrency conflict: expected {strict_expected}, found {current_version}')
        row = EventStoreModel(aggregate_id=aggregate_id, aggregate_type=aggregate_type, event_type=event_type, event_data=event_data, version=current_version + 1, tenant_id=tenant_id, region_code=self._region_code, correlation_id=correlation_id)
        try:
            session.add(row)
            await session.flush()
        except IntegrityError as exc:
            raise EventStoreConcurrencyError('Concurrency conflict on append_event') from exc
        return self._to_entry(row)

    @staticmethod
    def _to_entry(row: EventStoreModel) -> EventStoreEntry:
        return EventStoreEntry(id=row.id, aggregate_id=row.aggregate_id, aggregate_type=row.aggregate_type, event_type=row.event_type, event_data=dict(row.event_data or {}), version=row.version, tenant_id=row.tenant_id, region_code=row.region_code, correlation_id=row.correlation_id, created_at=row.created_at)