import pytest

from app.modules.operations.domain.enums import OrderStatus
from app.modules.operations.domain.state_machine import assert_order_transition


def test_operational_flow_happy_path_transitions():
    assert_order_transition(OrderStatus.DRAFT, OrderStatus.SUBMITTED)
    assert_order_transition(OrderStatus.SUBMITTED, OrderStatus.IN_REVIEW)
    assert_order_transition(OrderStatus.IN_REVIEW, OrderStatus.AWAITING_PAYMENT)
    assert_order_transition(OrderStatus.AWAITING_PAYMENT, OrderStatus.PAID)
    assert_order_transition(OrderStatus.PAID, OrderStatus.COMPLETED)


def test_operational_flow_blocks_invalid_transition():
    with pytest.raises(ValueError):
        assert_order_transition(OrderStatus.DRAFT, OrderStatus.PAID)

