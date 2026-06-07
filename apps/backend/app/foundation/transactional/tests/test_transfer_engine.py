from __future__ import annotations

import asyncio
from uuid import uuid4

import pytest
from unittest.mock import AsyncMock

from apps.backend.app.foundation.transactional.core import TransferTransactionalEngine


@pytest.mark.asyncio
async def test_execute_transfer_calls_adapters() -> None:
    # Arrange: create mocks for capacity and enrollment adapters
    capacity = AsyncMock()
    enrollment_sm = AsyncMock()

    capacity.reserve.return_value = {"id": uuid4(), "capacity_reserved": 1}
    enrollment_sm.transition.return_value = {"id": uuid4(), "status": "TRANSFERRED"}

    engine = TransferTransactionalEngine(capacity=capacity, enrollment_sm=enrollment_sm)

    payload = {
        "institution_id": uuid4(),
        "grade": "10A",
        "shift": "MORNING",
        "current_enrollment_id": uuid4(),
        "actor_id": uuid4(),
    }

    # Act
    result = await engine.execute_transfer(session=None, payload=payload, idempotency_key="k")

    # Assert
    assert result["status"] == "success"
    capacity.reserve.assert_awaited_once()
    enrollment_sm.transition.assert_awaited_once()


@pytest.mark.asyncio
async def test_execute_transfer_no_capacity_raises() -> None:
    capacity = AsyncMock()
    enrollment_sm = AsyncMock()
    capacity.reserve.return_value = None

    engine = TransferTransactionalEngine(capacity=capacity, enrollment_sm=enrollment_sm)

    payload = {
        "institution_id": uuid4(),
        "grade": "10A",
        "shift": "MORNING",
        "current_enrollment_id": uuid4(),
        "actor_id": uuid4(),
    }

    try:
        await engine.execute_transfer(session=None, payload=payload, idempotency_key="k")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "No capacity" in str(exc)
