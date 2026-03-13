from enum import Enum


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"
    CONFIRMED = "confirmed"


class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class PaymentMethod(str, Enum):
    BNA = "bna"
    MULTICAIXA = "multicaixa"
    CASH = "cash"


class TransactionType(str, Enum):
    PAYMENT = "payment"
    REFUND = "refund"
