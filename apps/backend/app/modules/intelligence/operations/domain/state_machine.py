from app.modules.intelligence.operations.domain.enums import OrderStatus
VALID_ORDER_TRANSITIONS: dict[OrderStatus, set[OrderStatus]] = {OrderStatus.DRAFT: {OrderStatus.SUBMITTED}, OrderStatus.SUBMITTED: {OrderStatus.IN_REVIEW, OrderStatus.REJECTED}, OrderStatus.IN_REVIEW: {OrderStatus.AWAITING_PAYMENT, OrderStatus.REJECTED}, OrderStatus.AWAITING_PAYMENT: {OrderStatus.PAID, OrderStatus.REJECTED}, OrderStatus.PAID: {OrderStatus.COMPLETED}, OrderStatus.COMPLETED: set(), OrderStatus.REJECTED: set()}

def assert_order_transition(current: OrderStatus, target: OrderStatus) -> None:
    allowed = VALID_ORDER_TRANSITIONS.get(current, set())
    if target not in allowed:
        raise ValueError(f'Invalid order transition: {current.value} -> {target.value}')