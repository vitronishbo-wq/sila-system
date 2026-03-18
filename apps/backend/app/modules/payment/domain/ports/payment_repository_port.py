from abc import ABC, abstractmethod
from typing import List, Optional
from apps.backend.app.modules.payment.domain.models.payment import Payment

class PaymentRepositoryPort(ABC):
    """Port: Contract for Payment persistence."""

    @abstractmethod
    async def create(self, payment: Payment) -> Payment:
        """Create a new payment in storage."""
        pass

    @abstractmethod
    async def save(self, payment: Payment) -> Payment:
        """Save/update an existing payment."""
        pass

    @abstractmethod
    async def get_by_id(self, payment_id: str) -> Optional[Payment]:
        """Retrieve payment by ID."""
        pass

    @abstractmethod
    async def get_by_reference(self, reference: str) -> Optional[Payment]:
        """Retrieve payment by reference."""
        pass

    @abstractmethod
    async def list_by_citizen(self, citizen_id: str, limit: int=100, offset: int=0) -> List[Payment]:
        """List payments for a specific citizen."""
        pass

    @abstractmethod
    async def list_by_status(self, status: str, limit: int=100, offset: int=0) -> List[Payment]:
        """List payments filtered by status."""
        pass

    @abstractmethod
    async def list_all(self, limit: int=100, offset: int=0) -> List[Payment]:
        """List all payments with pagination."""
        pass

    @abstractmethod
    async def delete(self, payment_id: str) -> bool:
        """Delete a payment."""
        pass

    @abstractmethod
    async def exists(self, payment_id: str) -> bool:
        """Check if payment exists."""
        pass