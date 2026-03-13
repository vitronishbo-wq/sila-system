from __future__ import annotations

import hashlib
import hmac
import inspect
import json

from fastapi import HTTPException

from modules.payment.models.enums import PaymentStatus
from modules.payment.services.payment_service import PaymentService


class WebhookEngine:
    def __init__(self, db, secret: str):
        self.db = db
        self.secret = secret
        self.payment_service = PaymentService(db=db)

    def verify_signature(self, payload: bytes, signature: str) -> bool:
        expected = hmac.new(self.secret.encode(), payload, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature or "")

    async def process_event(self, provider: str, payload: dict, signature: str, raw_payload: bytes):
        if not self.verify_signature(raw_payload, signature):
            raise HTTPException(status_code=401, detail="Invalid signature")

        reference = payload.get("reference")
        event = (payload.get("event") or "").lower()
        payment = self.payment_service.get_by_reference(reference)
        if inspect.isawaitable(payment):
            payment = await payment
        if not payment:
            return {"detail": "Payment not found"}

        target = PaymentStatus.COMPLETED if event in {"success", "completed"} else PaymentStatus.FAILED
        if payment.status == target:
            return {"detail": "Event already processed"}

        result = self.payment_service.update_status(getattr(payment, "id", None), target)
        if inspect.isawaitable(result):
            await result
        return {"detail": f"Payment {reference} updated to {target.value}"}


class PaymentWebhookService:
    def __init__(self, db, payment_service):
        self.db = db
        self.payment_service = payment_service

    async def _log_event(self, **kwargs):
        return {"logged": True, **kwargs}

    @staticmethod
    def _verify_signature(secret: str, payload_body: bytes, signature: str) -> bool:
        expected = hmac.new(secret.encode(), payload_body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature or "")

    async def process_webhook(self, webhook_id: int, payload_body: bytes, headers: dict):
        config_result = await self.db.execute(("webhook_config", webhook_id))
        config = config_result.scalars().first()
        if not config or not getattr(config, "active", False):
            raise ValueError("Webhook config not found or inactive")

        signature = headers.get("X-Signature")
        secret = getattr(config, "secret_key", None)
        if secret and not self._verify_signature(secret, payload_body, signature):
            await self._log_event(status="error", reason="invalid_signature")
            raise ValueError("Invalid webhook signature")

        try:
            payload = json.loads(payload_body.decode())
        except Exception:
            await self._log_event(status="error", reason="invalid_json")
            raise ValueError("Invalid JSON payload")

        data = payload.get("data", {})
        reference = data.get("reference")
        if not reference:
            await self._log_event(status="skipped", reason="missing_reference")
            return {"status": "skipped", "reason": "Payment not found"}

        payment_result = await self.db.execute(("payment_reference", reference))
        payment = payment_result.scalars().first()
        if not payment:
            await self._log_event(status="skipped", reason="payment_not_found")
            return {"status": "skipped", "reason": "Payment not found"}

        status_map = {
            "completed": PaymentStatus.COMPLETED,
            "failed": PaymentStatus.FAILED,
            "pending": PaymentStatus.PENDING,
        }
        status_value = status_map.get(str(data.get("status", "pending")).lower(), PaymentStatus.PENDING)
        provider_reference = data.get("provider_id")

        await self.payment_service.update_payment_status(
            payment_id=getattr(payment, "id", None),
            status=status_value,
            provider_reference=provider_reference,
        )
        await self._log_event(status="success", payment_id=getattr(payment, "id", None))
        return {"status": "success"}
