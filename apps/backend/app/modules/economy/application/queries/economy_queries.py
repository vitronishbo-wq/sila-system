"""Economy domain queries."""
from dataclasses import dataclass
from typing import Optional

@dataclass
class GetInvoiceByIdQuery:
    """Query to retrieve invoice by ID."""
    invoice_id: str

@dataclass
class ListInvoicesByCitizenQuery:
    """Query to list invoices for citizen."""
    citizen_id: str
    limit: int = 100
    offset: int = 0

@dataclass
class ListPaymentsByCitizenQuery:
    """Query to list payments for citizen."""
    citizen_id: str
    limit: int = 100
    offset: int = 0