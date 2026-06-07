from __future__ import annotations

import asyncio
from types import SimpleNamespace
from uuid import uuid4

import pytest
from unittest.mock import AsyncMock

from apps.backend.app.foundation.transactional.adapters.sqlalchemy_capacity_adapter import (
    SQLAlchemyCapacityReservationAdapter,
)


@pytest.mark.asyncio
async def test_capacity_adapter_delegates_to_repository() -> None:
    adapter = SQLAlchemyCapacityReservationAdapter(session=None)

    inst_id = uuid4()
    grade = "10A"
    shift = "MORNING"

    mock_repo = SimpleNamespace(
        reserve_capacity=AsyncMock(return_value={"id": uuid4(), "capacity_reserved": 1}),
        release_capacity=AsyncMock(return_value={}),
        get_available=AsyncMock(return_value=5),
    )

    adapter.repo = mock_repo

    res = await adapter.reserve(None, inst_id, grade, shift, quantity=1)
    assert res is not None
    mock_repo.reserve_capacity.assert_awaited_once_with(inst_id, grade, shift, 1)

    avail = await adapter.get_available(None, inst_id, grade, shift)
    assert avail == 5
    mock_repo.get_available.assert_awaited_once_with(inst_id, grade, shift)

    await adapter.release(None, res["id"], quantity=1)
    mock_repo.release_capacity.assert_awaited_once_with(res["id"], 1)


@pytest.mark.asyncio
async def test_capacity_adapter_concurrent_reservations_simulation() -> None:
    """Simulate concurrent reservations using an in-memory fake repo with an asyncio.Lock.

    This is a proof-of-concurrency concept: the fake repo serializes access
    to emulate database-level FOR UPDATE behavior and ensures no overbooking.
    """

    class FakeRepo:
        def __init__(self, total: int):
            self.capacity_total = total
            self.capacity_used = 0
            self.capacity_reserved = 0
            self.lock = asyncio.Lock()

        async def reserve_capacity(self, institution_id, grade, shift, quantity):
            async with self.lock:
                available = self.capacity_total - self.capacity_used - self.capacity_reserved
                if available < quantity:
                    return None
                # simulate some processing delay
                await asyncio.sleep(0.01)
                self.capacity_reserved += quantity
                return {"id": uuid4(), "capacity_reserved": self.capacity_reserved}

        async def release_capacity(self, id, quantity):
            async with self.lock:
                self.capacity_reserved = max(0, self.capacity_reserved - quantity)
                return {"id": id, "capacity_reserved": self.capacity_reserved}

        async def get_available(self, institution_id, grade, shift):
            async with self.lock:
                return max(0, self.capacity_total - self.capacity_used - self.capacity_reserved)

    repo = FakeRepo(total=1)
    adapter = SQLAlchemyCapacityReservationAdapter(session=None)
    adapter.repo = repo

    inst_id = uuid4()
    grade = "10A"
    shift = "MORNING"

    async def try_reserve(i):
        r = await adapter.reserve(None, inst_id, grade, shift, quantity=1)
        return r is not None

    tasks = [try_reserve(i) for i in range(10)]
    results = await asyncio.gather(*tasks)

    # Only one task should succeed because total capacity is 1
    assert sum(1 for r in results if r) == 1
