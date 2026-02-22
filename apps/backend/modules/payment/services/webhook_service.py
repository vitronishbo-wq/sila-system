"""Service for handling payment method webhooks."""

import hmac
import hashlib
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from modules.payment.models.webhook import PaymentWebhook
from modules.payment.models.webhook_event import PaymentWebhookEvent
from modules.payment.models.payment import Payment
from modules.payment.models.enums import PaymentStatus, TransactionStatus
from modules.payment.services.payment_service import PaymentService

logger = logging.getLogger(__name__)


class PaymentWebhookService:
    """Service to handle incoming payment webhooks."""

    def __init__(self, db: AsyncSession, payment_service: PaymentService):
        self.db = db
        self.payment_service = payment_service

    async def _get_webhook_config(self, webhook_id: int) -> Optional[PaymentWebhook]:
        """Get webhook configuration by ID."""
        result = await self.db.execute(
            select(PaymentWebhook).where(PaymentWebhook.id == webhook_id)
        )
        return result.scalars().first()

    def _verify_signature(self, payload: bytes, secret: str, signature: str) -> bool:
        """Verify HMAC signature of the payload."""
        if not secret:
            return True  # If no secret configured, skip validation (use with caution)

        expected_signature = hmac.new(
            secret.encode(), payload, hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_signature, signature)

    async def process_webhook(
        self, webhook_id: int, payload_body: bytes, headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Process an incoming webhook.

        Args:
            webhook_id: ID of the webhook configuration to use.
            payload_body: Raw body bytes for signature verification.
            headers: Request headers containing signature.

        Returns:
            Dict containing processing result details.
        """
        # 1. Get Config
        webhook_config = await self._get_webhook_config(webhook_id)
        if not webhook_config or not webhook_config.active:
            raise ValueError(f"Webhook config {webhook_id} not found or inactive")

        # 2. Verify Signature (assuming generic 'X-Signature' header, logic may vary by provider)
        signature = headers.get("X-Signature") or headers.get("x-signature")
        if webhook_config.secret_key:
            if not signature or not self._verify_signature(
                payload_body, webhook_config.secret_key, signature
            ):
                await self._log_event(
                    webhook_id,
                    "signature_verification_failed",
                    {"headers": dict(headers)},
                    error="Invalid signature",
                )
                raise ValueError("Invalid webhook signature")

        try:
            payload_json = json.loads(payload_body)
        except json.JSONDecodeError:
            await self._log_event(
                webhook_id, "payload_error", {"body": str(payload_body)}, error="Invalid JSON"
            )
            raise ValueError("Invalid JSON payload")

        # 3. Extract Payment Info (Generic structure assumed, would need adapter for specific providers)
        # Expected format: {"event": "payment.completed", "data": {"reference": "PAY-123", "status": "COMPLETED"}}
        event_type = payload_json.get("event", "unknown")
        data = payload_json.get("data", {})
        reference = data.get("reference")
        new_status_str = data.get("status")

        if not reference:
            await self._log_event(
                webhook_id, event_type, payload_json, error="Missing payment reference"
            )
            raise ValueError("Missing payment reference in payload")

        # Find payment by reference
        payment_query = await self.db.execute(
            select(Payment).where(Payment.reference == reference)
        )
        payment = payment_query.scalars().first()

        if not payment:
            await self._log_event(
                webhook_id, event_type, payload_json, error=f"Payment {reference} not found"
            )
            return {"status": "skipped", "reason": "Payment not found"}

        # 4. Map Status and Update
        if new_status_str:
            try:
                # Simple mapping - real world might need a mapper function
                new_status = PaymentStatus(new_status_str.lower())

                # Use PaymentService to handle business logic (transitions, etc)
                if payment.status != new_status:
                    await self.payment_service.update_payment_status(
                        payment_id=payment.id,
                        status=new_status,
                        provider_reference=data.get("provider_id")
                    )
            except ValueError:
                logger.warning(f"Unknown status received: {new_status_str}")

        # 5. Log Success
        event_log = await self._log_event(
            webhook_id=webhook_id,
            event_type=event_type,
            payload=payload_json,
            payment_id=payment.id,
            delivered=True
        )

        return {"status": "success", "event_id": event_log.id}

    async def _log_event(
        self,
        webhook_id: int,
        event_type: str,
        payload: Dict,
        payment_id: Optional[int] = None,
        delivered: bool = False,
        error: Optional[str] = None,
    ) -> PaymentWebhookEvent:
        """Log the webhook event to database."""
        event = PaymentWebhookEvent(
            webhook_id=webhook_id,
            payment_id=payment_id,
            event_type=event_type,
            payload=payload,
            delivered=delivered,
            last_error=error,
            created_at=datetime.now(timezone.utc),
            delivered_at=datetime.now(timezone.utc) if delivered else None
        )

        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event


class WebhookEngine:
    """Compact and immediately executable Webhook Engine."""

    def __init__(self, db: AsyncSession, secret: str):
        self.db = db
        self.secret = secret
        self.payment_service = PaymentService(db)

    def verify_signature(self, payload: bytes, signature: str) -> bool:
        """HMAC verification (generic - works for Stripe, Paystack, etc.)"""
        if not signature:
            return False
        expected = hmac.new(self.secret.encode(), payload, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    async def process_event(
        self, provider: str, payload: Dict, signature: str, raw_payload: bytes
    ):
        # 1. Validate signature
        if not self.verify_signature(raw_payload, signature):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature"
            )

        # 2. Extract payment reference or external ID
        external_id = (
            payload.get("reference")
            or payload.get("id")
            or payload.get("data", {}).get("reference")
        )
        if not external_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing payment reference",
            )

        # 3. Find payment by reference (idempotent)
        payment = await self.payment_service.get_by_reference(external_id)
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found"
            )

        # 4. Determine event type and update status
        event_type = (
            payload.get("event") or payload.get("type") or payload.get("data", {}).get("status")
        )
        if not event_type:
            return {"detail": "Event ignored (missing type)"}

        status_map = {
            "success": PaymentStatus.COMPLETED,
            "succeeded": PaymentStatus.COMPLETED,
            "completed": PaymentStatus.COMPLETED,
            "failed": PaymentStatus.FAILED,
            "cancelled": PaymentStatus.CANCELLED,
            "pending": PaymentStatus.PROCESSING,
        }

        new_status = status_map.get(event_type.lower())
        if not new_status:
            return {"detail": f"Event ignored (unknown type: {event_type})"}

        # 5. Idempotent update
        if payment.status == new_status:
            return {"detail": "Event already processed"}

        await self.payment_service.update_status(payment.id, new_status)

        return {"detail": f"Payment {payment.reference} updated to {new_status.value}"}
