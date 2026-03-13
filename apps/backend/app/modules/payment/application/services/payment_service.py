from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from apps.backend.app.modules.payment.models.enums import (
    PaymentMethod,
    PaymentStatus,
    TransactionStatus,
    TransactionType,
)
from apps.backend.app.modules.payment.schemas.payment import RefundResponse


class Payment:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.amount = kwargs.get("amount", Decimal("0"))
        self.currency = kwargs.get("currency", "AOA")
        self.status = kwargs.get("status", PaymentStatus.PENDING)
        self.method = kwargs.get("method", PaymentMethod.BNA)
        self.reference = kwargs.get("reference")
        self.description = kwargs.get("description")
        self.metadata_ = kwargs.get("metadata_", {})
        self.created_at = kwargs.get("created_at", datetime.now(timezone.utc))
        self.updated_at = kwargs.get("updated_at", datetime.now(timezone.utc))


class PaymentTransaction:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.payment_id = kwargs.get("payment_id")
        self.amount = kwargs.get("amount", Decimal("0"))
        self.currency = kwargs.get("currency", "AOA")
        self.type = kwargs.get("type", TransactionType.PAYMENT)
        self.status = kwargs.get("status", TransactionStatus.PENDING)
        self.reference = kwargs.get("reference")
        self.provider_reference = kwargs.get("provider_reference")
        self.metadata_ = kwargs.get("metadata_", {})
        self.created_at = kwargs.get("created_at", datetime.now(timezone.utc))


class PaymentService:
    def __init__(self, db):
        self.db = db

    def _is_valid_status_transition(self, current: PaymentStatus, target: PaymentStatus) -> bool:
        valid = {
            PaymentStatus.PENDING: {PaymentStatus.PROCESSING, PaymentStatus.CANCELLED},
            PaymentStatus.PROCESSING: {
                PaymentStatus.COMPLETED,
                PaymentStatus.CANCELLED,
                PaymentStatus.FAILED,
            },
            PaymentStatus.COMPLETED: {PaymentStatus.REFUNDED, PaymentStatus.PARTIALLY_REFUNDED},
            PaymentStatus.CANCELLED: set(),
            PaymentStatus.FAILED: set(),
            PaymentStatus.REFUNDED: set(),
            PaymentStatus.PARTIALLY_REFUNDED: {PaymentStatus.REFUNDED},
            PaymentStatus.CONFIRMED: {PaymentStatus.COMPLETED},
        }
        return target in valid.get(current, set())

    async def _generate_reference(self, prefix: str = "PAY") -> str:
        return f"{prefix}-{uuid4().hex[:8].upper()}"

    async def _get_latest_transaction(self, payment_id: int):
        result = await self.db.execute(("latest_transaction", payment_id))
        return result.scalars().first()

    async def create_payment(self, payment_data, user_id: int):
        reference = await self._generate_reference("PAY")
        payment = Payment(
            amount=payment_data.amount,
            currency=payment_data.currency,
            status=PaymentStatus.PENDING,
            method=payment_data.method,
            reference=reference,
            description=payment_data.description,
            metadata_=payment_data.metadata,
        )
        self.db.add(payment)
        await self.db.flush()

        tx = PaymentTransaction(
            payment_id=getattr(payment, "id", None),
            amount=payment_data.amount,
            currency=payment_data.currency,
            type=TransactionType.PAYMENT,
            status=TransactionStatus.PENDING,
            reference=reference,
            metadata_={"user_id": user_id},
        )
        self.db.add(tx)
        await self.db.commit()
        await self.db.refresh(payment)
        return payment

    async def get_payment(self, payment_id: int):
        result = await self.db.execute(("payment_by_id", payment_id))
        return result.scalars().first()

    async def get_by_reference(self, reference: str):
        result = await self.db.execute(("payment_by_reference", reference))
        return result.scalars().first()

    async def update_status(self, payment_id: int, status: PaymentStatus):
        return await self.update_payment_status(payment_id, status)

    async def update_payment_status(
        self,
        payment_id: int,
        status: PaymentStatus,
        provider_reference: str | None = None,
    ):
        payment = await self.get_payment(payment_id)
        if payment is None:
            return None

        current = payment.status if isinstance(payment.status, PaymentStatus) else PaymentStatus(payment.status)
        if not self._is_valid_status_transition(current, status):
            raise ValueError("Invalid status transition")

        payment.status = status
        payment.updated_at = datetime.now(timezone.utc)
        tx = await self._get_latest_transaction(payment_id)
        if tx is not None:
            if status == PaymentStatus.COMPLETED:
                tx.status = TransactionStatus.COMPLETED
            elif status == PaymentStatus.FAILED:
                tx.status = TransactionStatus.FAILED
            if provider_reference:
                tx.provider_reference = provider_reference

        await self.db.commit()
        return payment

    async def create_refund(self, payment_id: int, refund_data, user_id: int):
        payment = await self.get_payment(payment_id)
        if payment is None:
            raise ValueError("Payment not found")

        if payment.status not in {PaymentStatus.COMPLETED, PaymentStatus.PARTIALLY_REFUNDED}:
            raise ValueError("Can only refund completed payments")

        payment_amount = Decimal(str(payment.amount))
        refund_amount = payment_amount if refund_data.amount is None else Decimal(str(refund_data.amount))

        if refund_amount > payment_amount:
            raise ValueError("Refund amount cannot exceed payment amount")

        reference = await self._generate_reference("RFD")
        tx = PaymentTransaction(
            payment_id=payment_id,
            amount=refund_amount,
            currency=payment.currency,
            type=TransactionType.REFUND,
            status=TransactionStatus.PENDING,
            reference=reference,
            metadata_={"user_id": user_id, "reason": refund_data.reason},
        )
        self.db.add(tx)
        payment.status = (
            PaymentStatus.REFUNDED
            if refund_amount == payment_amount
            else PaymentStatus.PARTIALLY_REFUNDED
        )
        payment.updated_at = datetime.now(timezone.utc)
        await self.db.commit()

        return RefundResponse(
            amount=float(refund_amount),
            status=TransactionStatus.PENDING,
            reference=reference,
        )

    async def delete_payment(self, payment_id: int, user_id: int):
        payment = await self.get_payment(payment_id)
        if payment is None:
            return False
        await self.db.delete(payment)
        await self.db.commit()
        return True
