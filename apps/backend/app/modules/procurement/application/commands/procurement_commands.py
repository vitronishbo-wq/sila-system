"""Procurement domain commands."""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass
class CreateTenderCommand:
    """Command to create a tender."""
    title: str
    description: str
    budget: Decimal
    deadline: str
    metadata: Optional[dict] = None

@dataclass
class SubmitBidCommand:
    """Command to submit a bid."""
    tender_id: str
    supplier_id: str
    amount: Decimal
    proposal: str
    metadata: Optional[dict] = None

@dataclass
class AwardContractCommand:
    """Command to award contract."""
    tender_id: str
    supplier_id: str
    bid_id: str
    metadata: Optional[dict] = None

@dataclass
class CreateSupplierCommand:
    """Command to register supplier."""
    name: str
    tax_id: str
    contact: str
    metadata: Optional[dict] = None