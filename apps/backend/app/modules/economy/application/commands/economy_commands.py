"""Economy domain commands."""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass
class CreateInvoiceCommand:
    """Command to create an invoice."""
    citizen_id: str
    reference: str
    amount: Decimal
    description: Optional[str] = None
    metadata: Optional[dict] = None

@dataclass
class ProcessInvoiceCommand:
    """Command to process/finalize an invoice."""
    invoice_id: str
    status: str
    metadata: Optional[dict] = None

@dataclass
class CreatePaymentCommand:
    """Command to record payment for invoice."""
    invoice_id: str
    amount: Decimal
    method: str
    reference: Optional[str] = None
    metadata: Optional[dict] = None