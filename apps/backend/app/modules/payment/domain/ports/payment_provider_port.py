from abc import ABC, abstractmethod
from typing import Any

from ..models.payment import Payment


class PaymentProviderPort(ABC):
    """Port: Contract for external payment provider integration."""

    @abstractmethod
    async def authorize(self, payment: Payment) -> dict[str, Any]:
        """Authorize a payment with external provider."""
        pass

    @abstractmethod
    async def capture(self, provider_reference: str) -> dict[str, Any]:
        """Capture an authorized payment."""
        pass

    @abstractmethod
    async def refund(self, provider_reference: str, amount: float | None = None) -> dict[str, Any]:
        """Request refund from external provider."""
        pass

    @abstractmethod
    async def verify_webhook(self, signature: str, payload: str) -> bool:
        """Verify webhook signature from payment provider."""
        pass

    @abstractmethod
    async def parse_webhook(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Parse webhook payload from payment provider."""
        pass

    @abstractmethod
    async def get_transaction_status(self, provider_reference: str) -> str:
        """Query transaction status from provider."""
        pass
