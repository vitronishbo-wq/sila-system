from datetime import UTC, datetime, timezone
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from apps.backend.app.modules.operations.application.services.operations_service import (
    OperationsService,
)
from apps.backend.app.modules.operations.domain.enums import OrderStatus, PaymentStatus


def _session_with_scalar_first(first_value):
    db = AsyncMock()
    result = MagicMock()
    scalars = MagicMock()
    scalars.first.return_value = first_value
    result.scalars.return_value = scalars
    db.execute = AsyncMock(return_value=result)
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.add = MagicMock()
    return db


@pytest.mark.asyncio
async def test_confirm_payment_is_idempotent_when_already_confirmed():
    payment = SimpleNamespace(
        id=uuid4(),
        status=PaymentStatus.CONFIRMED.value,
        reference="SIM-ABC",
        provider="FAKE_BANK",
        order=SimpleNamespace(status=OrderStatus.PAID.value),
        confirmed_at=datetime.now(UTC),
    )
    db = _session_with_scalar_first(payment)
    service = OperationsService(db)

    result = await service.confirm_payment(payment.reference)

    assert result is payment
    db.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_confirm_payment_rejects_failed_payment():
    payment = SimpleNamespace(
        id=uuid4(),
        status=PaymentStatus.FAILED.value,
        reference="SIM-FAILED",
        provider="FAKE_BANK",
        order=SimpleNamespace(status=OrderStatus.AWAITING_PAYMENT.value),
    )
    db = _session_with_scalar_first(payment)
    service = OperationsService(db)

    with pytest.raises(ValueError, match="Failed payment cannot be confirmed"):
        await service.confirm_payment(payment.reference)

    db.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_generate_payment_reuses_existing_pending_reference():
    order_id = uuid4()
    citizen_id = uuid4()
    order = SimpleNamespace(
        id=order_id,
        citizen_id=citizen_id,
        status=OrderStatus.AWAITING_PAYMENT.value,
        total_amount=Decimal("2500.00"),
    )
    existing_payment = SimpleNamespace(
        id=uuid4(),
        order_id=order_id,
        reference="SIM-EXISTING",
        status=PaymentStatus.PENDING.value,
    )
    db = _session_with_scalar_first(existing_payment)
    service = OperationsService(db)
    service._get_order_for_update = AsyncMock(return_value=order)
    service._transition_order = MagicMock()

    result = await service.generate_payment(order_id, citizen_id)

    assert result is existing_payment
    service._transition_order.assert_not_called()
    db.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_complete_order_is_idempotent_when_already_completed():
    order_id = uuid4()
    citizen_id = uuid4()
    order = SimpleNamespace(
        id=order_id,
        citizen_id=citizen_id,
        status=OrderStatus.COMPLETED.value,
        proof_payload={"receipt_number": "RCP-001"},
    )
    service = OperationsService(AsyncMock())
    service._get_order_for_update = AsyncMock(return_value=order)
    service._get_order = AsyncMock(return_value=order)
    service._transition_order = MagicMock()

    result = await service.complete_order(order_id, citizen_id)

    assert result is order
    service._transition_order.assert_not_called()


@pytest.mark.asyncio
async def test_complete_order_requires_paid_state():
    order_id = uuid4()
    citizen_id = uuid4()
    order = SimpleNamespace(
        id=order_id,
        citizen_id=citizen_id,
        service_id=uuid4(),
        total_amount=Decimal("1000.00"),
        status=OrderStatus.IN_REVIEW.value,
        status_history=[],
        receipt_number=None,
        proof_payload=None,
    )
    service = OperationsService(AsyncMock())
    service._get_order_for_update = AsyncMock(return_value=order)

    with pytest.raises(ValueError, match="Invalid order transition"):
        await service.complete_order(order_id, citizen_id)
