import hashlib
import hmac
import json
import logging
from datetime import datetime, timezone
from typing import Any, Optional

from apps.backend.app.core.settings import settings
from apps.backend.app.modules.payment.domain.models.payment import Payment
from apps.backend.app.modules.payment.domain.ports.payment_provider_port import (
    PaymentProviderPort,
)
from apps.backend.app.platform.integration.models import ProviderCapability, ProviderStatus
from apps.backend.app.platform.integration.provider_base import ProviderBase
from apps.backend.app.platform.integration.provider_registry import ProviderRegistry

logger = logging.getLogger(__name__)


class MulticaixaRealProvider(PaymentProviderPort, ProviderBase):
    provider_name = "multicaixa"

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        merchant_id: Optional[str] = None,
        webhook_secret: Optional[str] = None,
        timeout: float = 30.0,
    ):
        ProviderBase.__init__(
            self,
            base_url=base_url or settings.MULTICAIXA_BASE_URL,
            api_key=api_key or settings.MULTICAIXA_API_KEY,
            timeout=timeout,
        )
        self._merchant_id = merchant_id or settings.MULTICAIXA_MERCHANT_ID
        self._webhook_secret = webhook_secret or settings.MULTICAIXA_WEBHOOK_SECRET

    def _headers(self, method: str, path: str, body: str = "") -> dict[str, str]:
        timestamp = str(int(datetime.now(timezone.utc).timestamp()))
        message = f"{method}:{path}:{timestamp}:{body}"
        signature = hmac.new(
            self.api_key.encode(), message.encode(), hashlib.sha256
        ).hexdigest()
        return {
            "X-Multicaixa-Api-Key": self.api_key,
            "X-Multicaixa-Timestamp": timestamp,
            "X-Multicaixa-Signature": signature,
            "X-Multicaixa-Merchant-Id": self._merchant_id,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def health_check(self) -> dict[str, Any]:
        return await self._request("GET", "/health", headers=self._headers("GET", "/health"))

    async def authorize(self, payment: Payment) -> dict[str, Any]:
        body = json.dumps({
            "payment_id": str(payment.id),
            "reference": payment.reference,
            "merchant_id": self._merchant_id,
        })
        return await self._request(
            "POST", "/payments/authorize",
            json_data={"payment_id": str(payment.id), "reference": payment.reference},
            headers=self._headers("POST", "/payments/authorize", body),
        )

    async def capture(self, provider_reference: str) -> dict[str, Any]:
        body = json.dumps({"provider_reference": provider_reference})
        return await self._request(
            "POST", f"/payments/{provider_reference}/capture",
            json_data={"provider_reference": provider_reference},
            headers=self._headers("POST", f"/payments/{provider_reference}/capture", body),
        )

    async def refund(self, provider_reference: str, amount: Optional[float] = None) -> dict[str, Any]:
        data = {"provider_reference": provider_reference}
        if amount is not None:
            data["amount"] = amount
        body = json.dumps(data)
        return await self._request(
            "POST", f"/payments/{provider_reference}/refund",
            json_data=data,
            headers=self._headers("POST", f"/payments/{provider_reference}/refund", body),
        )

    async def verify_webhook(self, signature: str, payload: str) -> bool:
        expected = hmac.new(
            self._webhook_secret.encode(), payload.encode(), hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, expected)

    async def parse_webhook(self, payload: dict) -> dict[str, Any]:
        return {
            "provider": "multicaixa",
            "event": payload.get("event", "unknown"),
            "reference": payload.get("reference", ""),
            "status": payload.get("status", "pending"),
            "amount": payload.get("amount"),
            "timestamp": payload.get("timestamp"),
        }

    async def get_transaction_status(self, provider_reference: str) -> str:
        result = await self._request(
            "GET", f"/payments/{provider_reference}",
            headers=self._headers("GET", f"/payments/{provider_reference}"),
        )
        return result.get("status", "unknown")


def create_multicaixa_provider() -> PaymentProviderPort:
    from apps.backend.app.platform.integration.helpers import is_placeholder_key

    has_creds = settings.MULTICAIXA_API_KEY and settings.MULTICAIXA_MERCHANT_ID

    if settings.PROVIDER_MODE == "homologation" and has_creds:
        ProviderRegistry.register(
            "multicaixa", ProviderCapability.PAYMENT,
            status=ProviderStatus.HOMOLOGATION, version="1.0.0",
            mock_reason="Homologação institucional — credenciais de staging",
        )
        logger.info("multicaixa_provider=homologation")
        return MulticaixaRealProvider()

    if has_creds:
        if is_placeholder_key(settings.MULTICAIXA_API_KEY) or is_placeholder_key(settings.MULTICAIXA_MERCHANT_ID):
            ProviderRegistry.register(
                "multicaixa", ProviderCapability.PAYMENT,
                status=ProviderStatus.MOCK_LIVE, version="0.0.0",
                mock_reason="MOCK ao vivo — credenciais com placeholder",
            )
            logger.info("multicaixa_provider=mock_live (placeholder)")
            from apps.backend.app.modules.payment.infrastructure.adapters.multicaixa_provider import (
                MulticaixaMockProvider,
            )
            return MulticaixaMockProvider()
        ProviderRegistry.register(
            "multicaixa", ProviderCapability.PAYMENT,
            status=ProviderStatus.REAL, version="1.0.0",
        )
        logger.info("multicaixa_provider=real")
        return MulticaixaRealProvider()

    ProviderRegistry.register(
        "multicaixa", ProviderCapability.PAYMENT,
        status=ProviderStatus.MOCK, version="0.0.0",
        mock_reason="Sem credenciais configuradas",
    )
    logger.info("multicaixa_provider=mock (sem credenciais)")
    from apps.backend.app.modules.payment.infrastructure.adapters.multicaixa_provider import (
        MulticaixaMockProvider,
    )
    return MulticaixaMockProvider()
