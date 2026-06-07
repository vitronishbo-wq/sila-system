from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from apps.backend.app.core.catalog.models.service import Service
from apps.backend.app.modules.intelligence.operations.domain.enums import OrderStatus, PaymentStatus
from apps.backend.app.modules.intelligence.operations.domain.state_machine import (
    assert_order_transition,
)
from apps.backend.app.modules.intelligence.operations.infrastructure.models.order_model import (
    OperationalOrderDocumentModel,
    OperationalOrderModel,
)
from apps.backend.app.modules.intelligence.operations.infrastructure.models.payment_model import (
    OperationalPaymentModel,
)


class OperationsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_services(self) -> list[dict]:
        stmt = (
            select(Service)
            .options(selectinload(Service.module))
            .where(
                Service.is_active.is_(True),
                or_(Service.is_public.is_(True), Service.scope == "public"),
            )
            .order_by(Service.business_priority.asc(), Service.name.asc())
        )
        rows = (await self.db.execute(stmt)).scalars().all()
        result = []
        for row in rows:
            description = row.description or f"Servico {row.name}"
            workflow_key = getattr(row, "workflow_definition_key", None) or row.code
            required_documents = list(getattr(row, "required_documents", []) or [])
            module_slug = row.module.slug if row.module else None
            module_title = row.module.title if row.module else None
            visibility = getattr(row, "visibility", None) or (
                "PUBLIC" if row.is_public else "INTERNAL"
            )
            result.append(
                {
                    "id": row.id,
                    "code": row.code,
                    "name": row.name,
                    "description": description,
                    "price": float(row.price or 0),
                    "estimated_days": row.estimated_days,
                    "workflow_definition_key": workflow_key,
                    "required_documents": required_documents,
                    "visibility": visibility,
                    "version": int(getattr(row, "version", 1) or 1),
                    "module_slug": module_slug,
                    "module_title": module_title,
                    "is_essential": bool(row.is_essential),
                    "icon_slug": row.icon_slug,
                    "active": bool(row.is_active),
                }
            )
        return result

    async def create_order(self, citizen_id: UUID, service_id: UUID) -> OperationalOrderModel:
        service = await self.db.get(Service, service_id)
        if not service or not service.is_active:
            raise ValueError("Service not found or inactive")
        amount = Decimal(service.price or 0)
        order = OperationalOrderModel(
            citizen_id=citizen_id,
            service_id=service.id,
            workflow_instance_id=uuid4(),
            total_amount=amount,
            status=OrderStatus.DRAFT.value,
            status_history=[self._history_entry(None, OrderStatus.DRAFT.value, "Order created")],
        )
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)
        return await self._get_order(order.id, citizen_id)

    async def add_documents(
        self, order_id: UUID, citizen_id: UUID, documents: list[dict]
    ) -> OperationalOrderModel:
        order = await self._get_order(order_id, citizen_id)
        if order.status != OrderStatus.DRAFT.value:
            raise ValueError("Documents can only be attached while order is DRAFT")
        for item in documents:
            doc = OperationalOrderDocumentModel(
                order_id=order.id,
                filename=item["filename"],
                content_type=item["content_type"],
                size_bytes=item["size_bytes"],
                uri=item.get("uri"),
            )
            self.db.add(doc)
        await self.db.commit()
        return await self._get_order(order_id, citizen_id)

    async def submit_order(self, order_id: UUID, citizen_id: UUID) -> OperationalOrderModel:
        order = await self._get_order(order_id, citizen_id)
        if not order.documents:
            raise ValueError("At least one document is required before submission")
        self._transition_order(order, OrderStatus.SUBMITTED, "Citizen submitted order")
        order.submitted_at = datetime.now(UTC)
        self._transition_order(order, OrderStatus.IN_REVIEW, "Order moved to review queue")
        await self.db.commit()
        return await self._get_order(order_id, citizen_id)

    async def generate_payment(self, order_id: UUID, citizen_id: UUID) -> OperationalPaymentModel:
        order = await self._get_order_for_update(order_id, citizen_id)
        if order.status not in {OrderStatus.IN_REVIEW.value, OrderStatus.AWAITING_PAYMENT.value}:
            raise ValueError("Payment can only be generated from IN_REVIEW or AWAITING_PAYMENT")
        pending_stmt = select(OperationalPaymentModel).where(
            OperationalPaymentModel.order_id == order.id,
            OperationalPaymentModel.status == PaymentStatus.PENDING.value,
        )
        existing = (await self.db.execute(pending_stmt)).scalars().first()
        if existing:
            return existing
        reference = f"SIM-{order.id.hex[:8].upper()}-{uuid4().hex[:6].upper()}"
        payment = OperationalPaymentModel(
            order_id=order.id,
            reference=reference,
            amount=order.total_amount,
            status=PaymentStatus.PENDING.value,
            provider="FAKE_BANK",
        )
        self.db.add(payment)
        if order.status != OrderStatus.AWAITING_PAYMENT.value:
            self._transition_order(
                order, OrderStatus.AWAITING_PAYMENT, "Payment reference generated"
            )
        await self.db.commit()
        await self.db.refresh(payment)
        return payment

    async def confirm_payment(self, reference: str) -> OperationalPaymentModel:
        stmt = (
            select(OperationalPaymentModel)
            .options(selectinload(OperationalPaymentModel.order))
            .where(OperationalPaymentModel.reference == reference)
            .with_for_update()
        )
        payment = (await self.db.execute(stmt)).scalars().first()
        if not payment:
            raise ValueError("Payment reference not found")
        if payment.status == PaymentStatus.FAILED.value:
            raise ValueError("Failed payment cannot be confirmed")
        if payment.status == PaymentStatus.CONFIRMED.value:
            return payment
        now = datetime.now(UTC)
        if reference.startswith("SIM"):
            payment.status = PaymentStatus.CONFIRMED.value
            payment.confirmed_at = now
            payment.failure_reason = None
            if payment.order.status != OrderStatus.PAID.value:
                self._transition_order(
                    payment.order,
                    OrderStatus.PAID,
                    f"Payment confirmed by provider {payment.provider}",
                )
        else:
            payment.status = PaymentStatus.FAILED.value
            payment.failure_reason = "Gateway rejected payment reference"
        await self.db.commit()
        await self.db.refresh(payment)
        return payment

    async def complete_order(self, order_id: UUID, citizen_id: UUID) -> OperationalOrderModel:
        order = await self._get_order_for_update(order_id, citizen_id)
        if order.status == OrderStatus.COMPLETED.value and order.proof_payload:
            return await self._get_order(order_id, citizen_id)
        self._transition_order(order, OrderStatus.COMPLETED, "Order finished after payment")
        order.completed_at = datetime.now(UTC)
        if not order.receipt_number:
            order.receipt_number = f"RCP-{datetime.now(UTC):%Y%m%d}-{order.id.hex[:8].upper()}"
        order.proof_payload = {
            "receipt_number": order.receipt_number,
            "order_id": str(order.id),
            "citizen_id": str(order.citizen_id),
            "service_id": str(order.service_id),
            "amount": float(order.total_amount),
            "status": order.status,
            "issued_at": datetime.now(UTC).isoformat(),
        }
        await self.db.commit()
        return await self._get_order(order_id, citizen_id)

    async def get_order(self, order_id: UUID, citizen_id: UUID) -> OperationalOrderModel:
        return await self._get_order(order_id, citizen_id)

    async def get_receipt(self, order_id: UUID, citizen_id: UUID) -> dict:
        order = await self._get_order(order_id, citizen_id)
        if order.status != OrderStatus.COMPLETED.value or not order.proof_payload:
            raise ValueError("Order must be COMPLETED to emit receipt")
        return order.proof_payload

    async def _get_order(self, order_id: UUID, citizen_id: UUID) -> OperationalOrderModel:
        stmt = (
            select(OperationalOrderModel)
            .options(
                selectinload(OperationalOrderModel.documents),
                selectinload(OperationalOrderModel.payments),
            )
            .where(
                OperationalOrderModel.id == order_id, OperationalOrderModel.citizen_id == citizen_id
            )
        )
        order = (await self.db.execute(stmt)).scalars().first()
        if not order:
            raise ValueError("Order not found")
        return order

    async def _get_order_for_update(
        self, order_id: UUID, citizen_id: UUID
    ) -> OperationalOrderModel:
        stmt = (
            select(OperationalOrderModel)
            .options(
                selectinload(OperationalOrderModel.documents),
                selectinload(OperationalOrderModel.payments),
            )
            .where(
                OperationalOrderModel.id == order_id, OperationalOrderModel.citizen_id == citizen_id
            )
            .with_for_update()
        )
        order = (await self.db.execute(stmt)).scalars().first()
        if not order:
            raise ValueError("Order not found")
        return order

    def _transition_order(
        self, order: OperationalOrderModel, target_status: OrderStatus, reason: str
    ) -> None:
        current_status = OrderStatus(order.status)
        assert_order_transition(current_status, target_status)
        order.status = target_status.value
        history = list(order.status_history or [])
        history.append(self._history_entry(current_status.value, target_status.value, reason))
        order.status_history = history

    @staticmethod
    def _history_entry(from_status: str | None, to_status: str, reason: str) -> dict:
        return {
            "from": from_status,
            "to": to_status,
            "reason": reason,
            "at": datetime.now(UTC).isoformat(),
        }
