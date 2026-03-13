from __future__ import annotations
from datetime import date, timedelta
from decimal import Decimal
import os
from uuid import uuid4
import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from apps.backend.app.modules.resources.aguas_saneamento.application.events.fatura_events import FaturaEmitidaEvent
from apps.backend.app.modules.resources.aguas_saneamento.domain.models.fatura_agua import FaturaAgua
from apps.backend.app.modules.resources.aguas_saneamento.infrastructure.persistence.outbox import SQLAlchemyOutboxRepository

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
async def test_outbox_sqlalchemy_repository_roundtrip(db_session_factory):
    async with db_session_factory() as session:
        exists = await session.execute(text("SELECT to_regclass('aguas_saneamento_outbox_events')"))
        assert exists.scalar_one_or_none() is not None, 'Tabela fisica ausente: aguas_saneamento_outbox_events. Execute migration 20260304_040_aguas_saneamento_outbox_events.'
    repo = SQLAlchemyOutboxRepository(session_factory=db_session_factory)
    fatura = FaturaAgua.emitir(consumo_id=uuid4(), titular_id=uuid4(), referencia='2026-03', volume_m3=Decimal('12.50'), tarifa_m3=Decimal('23.40'), data_vencimento=date.today() + timedelta(days=7))
    fatura.numero_fatura = 'FAT/2026/000001'
    event = FaturaEmitidaEvent.from_fatura(fatura)
    saved = await repo.enqueue(event)
    assert saved.event_name == 'FaturaEmitida'
    assert saved.topic == 'aguas.fatura.emitida'
    assert saved.processed is False
    pending = await repo.get_pending(limit=10)
    assert len(pending) == 1
    assert pending[0].id == saved.id
    await repo.increment_retries(saved.id, error='broker timeout')
    pending = await repo.get_pending(limit=10)
    assert pending[0].retries == 1
    assert pending[0].last_error == 'broker timeout'
    await repo.mark_done(saved.id)
    pending = await repo.get_pending(limit=10)
    assert len(pending) == 0