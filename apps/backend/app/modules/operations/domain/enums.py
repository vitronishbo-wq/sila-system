from enum import StrEnum


class OrderStatus(StrEnum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    IN_REVIEW = "IN_REVIEW"
    AWAITING_PAYMENT = "AWAITING_PAYMENT"
    PAID = "PAID"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"


class PaymentStatus(StrEnum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    FAILED = "FAILED"
