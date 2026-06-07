"""Economy domain commands."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class CreateInvoiceCommand:
    """Command to create an invoice."""

    citizen_id: str
    reference: str
    amount: Decimal
    description: str | None = None
    metadata: dict | None = None


@dataclass
class ProcessInvoiceCommand:
    """Command to process/finalize an invoice."""

    invoice_id: str
    status: str
    metadata: dict | None = None


@dataclass
class CreatePaymentCommand:
    """Command to record payment for invoice."""

    invoice_id: str
    amount: Decimal
    method: str
    reference: str | None = None
    metadata: dict | None = None
