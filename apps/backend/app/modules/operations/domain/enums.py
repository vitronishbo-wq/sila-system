from enum import Enum

class OrderStatus(str, Enum):
    DRAFT = 'DRAFT'
    SUBMITTED = 'SUBMITTED'
    IN_REVIEW = 'IN_REVIEW'
    AWAITING_PAYMENT = 'AWAITING_PAYMENT'
    PAID = 'PAID'
    COMPLETED = 'COMPLETED'
    REJECTED = 'REJECTED'

class PaymentStatus(str, Enum):
    PENDING = 'PENDING'
    CONFIRMED = 'CONFIRMED'
    FAILED = 'FAILED'