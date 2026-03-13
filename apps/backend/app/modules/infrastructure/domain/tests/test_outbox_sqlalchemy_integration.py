from __future__ import annotations
import os
from decimal import Decimal
from uuid import uuid4
import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from app.modules.infrastructure.application.events.definitions import AditivoAssinadoEvent
from app.modules.infrastructure.infrastructure.persistence.outbox_repository import SQLAlchemyOutboxRepository

def _get_database_url() -> str:
    url = os.environ.get('DATABASE_URL', 'postgresql+asyncpg://sila_user:Trumanmarcelo_1983@127.0.0.1:5432/sila_db')
    if 'sqlite' in url:
        raise RuntimeError('Testes ORM reais exigem PostgreSQL')
    if url.startswith('postgresql://'):
        return url.replace('postgresql://', 'postgresql+asyncpg://', 1)
    return url

@pytest_asyncio.fixture
async def db_session_factory():
    engine = create_async_engine(_get_database_url(), echo=False, poolclass=NullPool)
    async with engine.connect() as conn:
        trans = await conn.begin()
        factory = sessionmaker(bind=conn, class_=AsyncSession, expire_on_commit=False, autocommit=False)
        try:
            yield factory
        finally:
            try:
                await trans.rollback()
            except Exception:
                pass
    await engine.dispose()

@pytest.mark.asyncio
@pytest.mark.integration
async def test_obras_publicas_outbox_repository_roundtrip(db_session_factory):
    async with db_session_factory() as session:
        exists = await session.execute(text("SELECT to_regclass('op_outbox_events')"))
        assert exists.scalar_one_or_none() is not None, 'Tabela fisica ausente: op_outbox_events. Execute migration 20260304_042_obras_publicas_outbox_events.'
    repo = SQLAlchemyOutboxRepository(session_factory=db_session_factory)
    event = AditivoAssinadoEvent.build(obra_id=uuid4(), codigo_obra='OBR/2026/000001', aditivo_id=uuid4(), tipo='prazo', valor_adicional=Decimal('1000.00'), prazo_adicional_dias=5)
    event_id = await repo.save(tenant_id='tenant-test', aggregate_type='Obra', aggregate_id=event.obra_id, event=event, correlation_id='corr-test')
    assert event_id is not None
