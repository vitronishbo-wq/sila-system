"""
Payment Module Domain Events
ACAO Compliance: All events track financial transactions and payments.
"""
from uuid import UUID
from datetime import date, datetime
from typing import Optional
from decimal import Decimal
from apps.backend.app.core.events.domain_event import DomainEvent, AuditableEvent, ComplianceEvent, StatusChangeEvent

class PaymentTransactionInitiated(AuditableEvent):
    """Emitted when a payment transaction is initiated."""
    transaction_id: UUID
    payer_id: UUID
    amount: Decimal
    currency: str = 'USD'
    transaction_date: datetime = None
    payment_method: str = ''

    def __post_init__(self):
        self.aggregate_type = 'PaymentTransaction'
        self.event_type = 'PaymentTransactionInitiated'
        super().__post_init__()

class PaymentProcessed(ComplianceEvent):
    """Emitted when payment is successfully processed (ACAO compliance)."""
    transaction_id: UUID
    payer_id: UUID
    payee_id: UUID
    amount: Decimal
    processing_date: date
    reference_number: str = ''

    def __post_init__(self):
        self.aggregate_type = 'PaymentTransaction'
        self.event_type = 'PaymentProcessed'
        super().__post_init__()

class PaymentStatusChanged(StatusChangeEvent):
    """Track payment status transitions (pending, approved, rejected, cleared)."""
    transaction_id: UUID
    reason: str = ''

    def __post_init__(self):
        self.aggregate_type = 'PaymentTransaction'
        self.event_type = 'PaymentStatusChanged'
        super().__post_init__()

class InvoiceIssued(ComplianceEvent):
    """Emitted when invoice is issued for payment."""
    invoice_id: UUID
    creditor_id: UUID
    debtor_id: UUID
    amount: Decimal
    issue_date: date
    due_date: date
    invoice_number: str = ''

    def __post_init__(self):
        self.aggregate_type = 'Invoice'
        self.event_type = 'InvoiceIssued'
        super().__post_init__()

class PaymentReconciled(ComplianceEvent):
    """Emitted when payment is reconciled with records."""
    reconciliation_id: UUID
    transaction_id: UUID
    reconciled_date: date
    reconciled_by: str = ''
    balance: Decimal = Decimal('0')

    def __post_init__(self):
        self.aggregate_type = 'PaymentReconciliation'
        self.event_type = 'PaymentReconciled'
        super().__post_init__()