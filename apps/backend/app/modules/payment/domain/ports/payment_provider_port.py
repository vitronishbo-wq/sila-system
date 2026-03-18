from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from apps.backend.app.modules.payment.domain.models.payment import Payment

class PaymentProviderPort(ABC):
    """Port: Contract for external payment provider integration."""

    @abstractmethod
    async def authorize(self, payment: Payment) -> Dict[str, Any]:
        """Authorize a payment with external provider."""
        pass

    @abstractmethod
    async def capture(self, provider_reference: str) -> Dict[str, Any]:
        """Capture an authorized payment."""
        pass

    @abstractmethod
    async def refund(self, provider_reference: str, amount: Optional[float]=None) -> Dict[str, Any]:
        """Request refund from external provider."""
        pass

    @abstractmethod
    async def verify_webhook(self, signature: str, payload: str) -> bool:
        """Verify webhook signature from payment provider."""
        pass

    @abstractmethod
    async def parse_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Parse webhook payload from payment provider."""
        pass

    @abstractmethod
    async def get_transaction_status(self, provider_reference: str) -> str:
        """Query transaction status from provider."""
        pass