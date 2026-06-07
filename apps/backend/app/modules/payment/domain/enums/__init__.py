"""Enumeradores para o domínio de Pagamentos."""

from enum import StrEnum


class PaymentStatus(StrEnum):
    """Estados do ciclo de vida de um pagamento."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    RECONCILED = "reconciled"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"
    DISPUTED = "disputed"


class PaymentMethod(StrEnum):
    """Métodos de pagamento suportados."""

    BNA = "bna"
    MULTICAIXA = "multicaixa"
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    CHEQUE = "cheque"
    DEBIT_CARD = "debit_card"
    CREDIT_CARD = "credit_card"
    INSTALLMENT_PLAN = "installment_plan"


class InvoiceStatus(StrEnum):
    """Estados do ciclo de vida de uma fatura."""

    DRAFT = "draft"
    ISSUED = "issued"
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    DISPUTED = "disputed"


class TransactionType(StrEnum):
    """Tipos de transações financeiras."""

    PAYMENT = "payment"
    REFUND = "refund"
    REVERSAL = "reversal"
    ADJUSTMENT = "adjustment"


class TransactionStatus(StrEnum):
    """Estados da transação no gateway de pagamento."""

    PENDING = "pending"
    AUTHORIZED = "authorized"
    SETTLED = "settled"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


__all__ = [
    "InvoiceStatus",
    "PaymentMethod",
    "PaymentStatus",
    "TransactionStatus",
    "TransactionType",
]
