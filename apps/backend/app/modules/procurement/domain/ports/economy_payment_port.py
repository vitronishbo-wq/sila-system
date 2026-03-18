"""
Payment Port - Interface for procurement to request fund releases from Economy Core.
Implements the hexagonal architecture boundary between Procurement and Economy modules.
"""
from abc import ABC, abstractmethod
from typing import Optional
from decimal import Decimal
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PaymentRequest:
    """Data transfer object for payment requests."""
    contract_id: str
    vendor_did: str
    amount: Decimal
    currency: str = 'AOA'
    description: str = ''
    metadata: dict = None

@dataclass
class PaymentResponse:
    """Data transfer object for payment responses."""
    payment_id: str
    contract_id: str
    status: str
    amount: Decimal
    settled_at: Optional[datetime] = None
    transaction_reference: str = ''
    error_reason: Optional[str] = None

class EconomyPaymentPort(ABC):
    """
    Abstract port for procurement to interact with Economy/Treasury.
    Ensures procurement never directly touches the Treasury database.
    All fund releases go through this controlled interface.
    """

    @abstractmethod
    async def request_funds(self, payment_request: PaymentRequest) -> PaymentResponse:
        """
        Request funds to be released for a contract.
        
        Args:
            payment_request: Details of the payment to authorize
            
        Returns:
            PaymentResponse with status and transaction reference
            
        Raises:
            InsufficientFundsError: Budget does not allow payment
            VendorNotValidError: Vendor DID not validated
            ContractNotFoundError: Contract does not exist
        """
        pass

    @abstractmethod
    async def get_payment_status(self, payment_id: str) -> PaymentResponse:
        """Get current status of a payment request."""
        pass

    @abstractmethod
    async def validate_vendor(self, vendor_did: str) -> bool:
        """
        Validate that a vendor/supplier is authorized to receive funds.
        Delegates to Identity module via X-Road.
        """
        pass

    @abstractmethod
    async def check_budget_availability(self, cost_center: str, amount: Decimal) -> bool:
        """
        Check if budget is available for a procurement.
        Called before creating a tender to fail fast.
        """
        pass