from __future__ import annotations

import asyncio
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from apps.backend.app.core.db import Base
from apps.backend.app.foundation.transactional.adapters.sqlalchemy_capacity_adapter import (
    SQLAlchemyCapacityReservationAdapter,
)
from apps.backend.app.modules.educacao.infrastructure.models.institution_capacity_model import (
    InstitutionCapacityModel,
)
from apps.backend.app.modules.educacao.infrastructure.repositories.sqlalchemy_capacity_repository import (
    SQLAlchemyCapacityRepository,
)


@pytest.mark.asyncio
async def test_sqlalchemy_capacity_adapter_forwards_calls() -> None:
    """The adapter should delegate CRUD operations to the underlying repository."""
    adapter = SQLAlchemyCapacityReservationAdapter(session=AsyncMock(spec=AsyncSession))
    adapter.repo = AsyncMock(spec=SQLAlchemyCapacityRepository)
    adapter.repo.reserve_capacity = AsyncMock(return_value={"id": uuid4(), "capacity_reserved": 1})
    adapter.repo.release_capacity = AsyncMock(return_value={"id": uuid4(), "capacity_reserved": 0})
    adapter.repo.get_available = AsyncMock(return_value=5)

    institution_id = uuid4()
    grade = "5"
    shift = "MORNING"

    result = await adapter.reserve(
        AsyncMock(spec=AsyncSession), institution_id, grade, shift, quantity=1
    )
    assert result["capacity_reserved"] == 1
    adapter.repo.reserve_capacity.assert_awaited_once_with(institution_id, grade, shift, 1)

    capacity_id = uuid4()
    result = await adapter.release(AsyncMock(spec=AsyncSession), capacity_id, quantity=1)
    assert result["capacity_reserved"] == 0
    adapter.repo.release_capacity.assert_awaited_once_with(capacity_id, 1)

    available = await adapter.get_available(AsyncMock(spec=AsyncSession), institution_id, grade, shift)
    assert available == 5
    adapter.repo.get_available.assert_awaited_once_with(institution_id, grade, shift)


@pytest.fixture
async def sqlite_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture
def async_session_factory(sqlite_engine: Any):
    return async_sessionmaker(sqlite_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.mark.asyncio
async def test_sqlalchemy_capacity_adapter_concurrent_reserve_does_not_overbook(
    async_session_factory: Any,
) -> None:
    """Simulate concurrent reserves and ensure the adapter does not overbook capacity."""
    institution_id = uuid4()
    grade = "5"
    shift = "MORNING"

    # Seed capacity record
    async with async_session_factory() as session:
        async with session.begin():
            repo = SQLAlchemyCapacityRepository(session)
            await repo.save(
                {
                    "id": uuid4(),
                    "institution_id": institution_id,
                    "grade": grade,
                    "shift": shift,
                    "capacity_total": 1,
                    "capacity_used": 0,
                    "capacity_reserved": 0,
                }
            )

    barrier = asyncio.Event()
    results: list[dict | None] = [None, None]

    async def reserve_task(index: int) -> None:
        async with async_session_factory() as session:
            adapter = SQLAlchemyCapacityReservationAdapter(session=session)
            await barrier.wait()
            async with session.begin():
                results[index] = await adapter.reserve(
                    session, institution_id, grade, shift, quantity=1
                )

    tasks = [asyncio.create_task(reserve_task(i)) for i in range(2)]
    barrier.set()
    await asyncio.gather(*tasks)

    reserved_count = sum(1 for item in results if item is not None)
    assert reserved_count == 1, "Only one concurrent reserve should succeed when capacity is 1"

    async with async_session_factory() as verify_session:
        repo = SQLAlchemyCapacityRepository(verify_session)
        capacity_row = await repo.get_by_institution_grade_shift(institution_id, grade, shift)
        assert capacity_row is not None
        assert capacity_row["capacity_reserved"] == 1
