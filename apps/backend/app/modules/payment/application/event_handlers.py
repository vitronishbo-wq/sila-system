"""
Payment Module Event Handlers
Handlers that process payment domain events.
"""

import logging
from collections.abc import Awaitable, Callable

from apps.backend.app.core.events.domain_event import DomainEvent
from apps.backend.app.modules.payment.domain.events import (
    InvoiceIssued,
    PaymentProcessed,
    PaymentReconciled,
    PaymentStatusChanged,
    PaymentTransactionInitiated,
)

logger = logging.getLogger(__name__)


async def handle_payment_transaction_initiated(event: PaymentTransactionInitiated) -> None:
    """Handler for PaymentTransactionInitiated events."""
    logger.info(f"Payment transaction initiated: {event.amount} {event.currency}")
    pass


async def handle_payment_processed(event: PaymentProcessed) -> None:
    """Handler for PaymentProcessed events (ACAO compliance)."""
    logger.info(f"Payment of {event.amount} processed successfully")
    pass


async def handle_payment_status_changed(event: PaymentStatusChanged) -> None:
    """Handler for PaymentStatusChanged events."""
    logger.info(f"Payment status changed: {event.old_status} -> {event.new_status}")
    pass


async def handle_invoice_issued(event: InvoiceIssued) -> None:
    """Handler for InvoiceIssued events (ACAO compliance)."""
    logger.info(f"Invoice {event.aggregate_id} issued for {event.amount}")
    pass


async def handle_payment_reconciled(event: PaymentReconciled) -> None:
    """Handler for PaymentReconciled events (ACAO compliance)."""
    logger.info(f"Payment reconciled with balance {event.balance}")
    pass


PAYMENT_EVENT_HANDLERS: dict[str, Callable[[DomainEvent], Awaitable[None]]] = {
    "PaymentTransactionInitiated": handle_payment_transaction_initiated,
    "PaymentProcessed": handle_payment_processed,
    "PaymentStatusChanged": handle_payment_status_changed,
    "InvoiceIssued": handle_invoice_issued,
    "PaymentReconciled": handle_payment_reconciled,
}
