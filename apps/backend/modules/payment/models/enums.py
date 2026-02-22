"""Enums para o módulo de pagamento."""

from enum import Enum


class BaseEnum(str, Enum):
    """
    Base class para enums representados como strings.

    Facilita a integração com SQLAlchemy e Pydantic.
    """

    def __str__(self) -> str:
        return self.value

    @classmethod
    def list_values(cls) -> list[str]:
        """Retorna uma lista com todos os valores do enum."""
        return [member.value for member in cls]


class PaymentStatus(BaseEnum):
    """Status de um pagamento."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"
    CANCELLED = "cancelled"


class PaymentMethod(BaseEnum):
    """Métodos de pagamento disponíveis."""

    BNA = "bna"
    UNITEL_MONEY = "unitel_money"
    M_PESA = "m_pesa"
    MULTICAIXA = "multicaixa"
    CREDIT_CARD = "credit_card"
    BANK_TRANSFER = "bank_transfer"
    CASH = "cash"


class TransactionType(BaseEnum):
    """Tipos de transação."""

    PAYMENT = "payment"
    REFUND = "refund"
    ADJUSTMENT = "adjustment"
    FEE = "fee"


class TransactionStatus(BaseEnum):
    """Status de uma transação."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REVERSED = "reversed"
    CANCELLED = "cancelled"
