"""Procurement domain queries."""
from dataclasses import dataclass

@dataclass
class GetTenderByIdQuery:
    """Query to retrieve tender by ID."""
    tender_id: str

@dataclass
class ListTendersByStatusQuery:
    """Query to list tenders by status."""
    status: str
    limit: int = 100
    offset: int = 0

@dataclass
class ListBidsForTenderQuery:
    """Query to list bids for tender."""
    tender_id: str
    limit: int = 100
    offset: int = 0

@dataclass
class GetSupplierByIdQuery:
    """Query to retrieve supplier by ID."""
    supplier_id: str

@dataclass
class ListAllSuppliersQuery:
    """Query to list all suppliers."""
    limit: int = 100
    offset: int = 0