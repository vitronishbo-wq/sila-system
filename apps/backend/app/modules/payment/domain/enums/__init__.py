"""Enumeradores para o domínio de Pagamentos."""
from enum import Enum


class PaymentStatus(str, Enum):
    """Estados do ciclo de vida de um pagamento."""
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    RECONCILED = 'reconciled'
    FAILED = 'failed'
    CANCELLED = 'cancelled'
    REFUNDED = 'refunded'
    DISPUTED = 'disputed'


class PaymentMethod(str, Enum):
    """Métodos de pagamento suportados."""
    CASH = 'cash'
    BANK_TRANSFER = 'bank_transfer'
    CHEQUE = 'cheque'
    DEBIT_CARD = 'debit_card'
    CREDIT_CARD = 'credit_card'
    INSTALLMENT_PLAN = 'installment_plan'
    MULTICAIXA = 'multicaixa'


class InvoiceStatus(str, Enum):
    """Estados do ciclo de vida de uma fatura."""
    DRAFT = 'draft'
    ISSUED = 'issued'
    PENDING = 'pending'
    PAID = 'paid'
    OVERDUE = 'overdue'
    CANCELLED = 'cancelled'
    DISPUTED = 'disputed'


class TransactionType(str, Enum):
    """Tipos de transações financeiras."""
    PAYMENT = 'payment'
    REFUND = 'refund'
    REVERSAL = 'reversal'
    ADJUSTMENT = 'adjustment'


class TransactionStatus(str, Enum):
    """Estados da transação no gateway de pagamento."""
    PENDING = 'pending'
    AUTHORIZED = 'authorized'
    SETTLED = 'settled'
    FAILED = 'failed'
    CANCELLED = 'cancelled'
    REFUNDED = 'refunded'


__all__ = [
    'PaymentStatus',
    'PaymentMethod',
    'InvoiceStatus',
    'TransactionType',
    'TransactionStatus',
]