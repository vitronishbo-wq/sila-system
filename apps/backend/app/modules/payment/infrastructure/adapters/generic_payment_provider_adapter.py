import hmac
import hashlib
from typing import Any, Dict, Optional
from apps.backend.app.modules.payment.domain.models.payment import Payment
from apps.backend.app.modules.payment.domain.ports.payment_provider_port import PaymentProviderPort

class GenericPaymentProviderAdapter(PaymentProviderPort):
    """Adapter: Generic payment provider implementation (base for real providers)."""

    def __init__(self, api_key: str, api_secret: str, endpoint: str=''):
        self.api_key = api_key
        self.api_secret = api_secret
        self.endpoint = endpoint

    async def authorize(self, payment: Payment) -> Dict[str, Any]:
        """Authorize a payment with provider."""
        return {'status': 'authorized', 'provider_reference': f'AUTH_{payment.id}', 'transaction_id': payment.id}

    async def capture(self, provider_reference: str) -> Dict[str, Any]:
        """Capture an authorized transaction."""
        return {'status': 'captured', 'provider_reference': provider_reference, 'timestamp': None}

    async def refund(self, provider_reference: str, amount: Optional[float]=None) -> Dict[str, Any]:
        """Request refund from provider."""
        return {'status': 'refund_initiated', 'provider_reference': provider_reference, 'original_reference': provider_reference, 'amount': amount}

    async def verify_webhook(self, signature: str, payload: str) -> bool:
        """Verify webhook signature (HMAC-SHA256)."""
        expected_signature = hmac.new(self.api_secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(signature, expected_signature)

    async def parse_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Parse webhook payload from provider."""
        return {'event_type': payload.get('event_type'), 'provider_reference': payload.get('reference'), 'status': payload.get('status'), 'amount': payload.get('amount'), 'timestamp': payload.get('timestamp')}

    async def get_transaction_status(self, provider_reference: str) -> str:
        """Query transaction status from provider."""
        return 'PENDING'