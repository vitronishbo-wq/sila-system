"""Procurement domain enums."""

from enum import Enum


class TenderStatus(Enum):
    """Tender status enumeration."""

    OPEN = "OPEN"
    CLOSED = "CLOSED"
    AWARDED = "AWARDED"
    CANCELLED = "CANCELLED"


class BidStatus(Enum):
    """Bid status enumeration."""

    SUBMITTED = "SUBMITTED"
    EVALUATED = "EVALUATED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class ContractStatus(Enum):
    """Contract status enumeration."""

    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    TERMINATED = "TERMINATED"
    SUSPENDED = "SUSPENDED"
