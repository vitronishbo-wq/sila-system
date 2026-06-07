"""Serviço simplificado de pagamentos compatível com a suíte atual."""

from __future__ import annotations

import inspect
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from apps.backend.app.modules.payment.application.dto.payment_schema import (
    CreatePaymentSchema,
    PaymentCreate,
    RefundCreate,
    RefundResponse,
)
from apps.backend.app.modules.payment.domain.enums import (
    InvoiceStatus,
    PaymentStatus,
    TransactionStatus,
    TransactionType,
)
from apps.backend.app.modules.payment.domain.exceptions import (
    DomainValidationError,
    DuplicatePaymentError,
    InvalidInvoiceStateError,
    InvoiceNotFoundError,
)
from apps.backend.app.modules.payment.domain.models import Payment as DomainPayment


@dataclass
class Payment:
    """Modelo leve usado pelos fluxos legados cobertos pela suíte atual."""

    amount: float
    currency: str
    method: str
    status: PaymentStatus
    reference: str
    description: str | None = None
    metadata_: dict[str, Any] = field(default_factory=dict)
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class PaymentTransaction:
    """Representação mínima de transação para testes e fluxos simples."""

    payment_id: int | str
    amount: float
    currency: str
    type: TransactionType
    status: TransactionStatus
    reference: str
    metadata_: dict[str, Any] = field(default_factory=dict)
    provider_reference: str | None = None


class PaymentService:
    """Serviço híbrido com suporte ao fluxo simples usado na suíte atual."""

    def __init__(
        self,
        db=None,
        payment_repository=None,
        invoice_repository=None,
        educacao_service=None,
        juventude_service=None,
        emprego_service=None,
        saude_service=None,
        assistencia_social_service=None,
        service_requests_service=None,
    ):
        self.db = db
        self.payment_repo = payment_repository
        self.invoice_repo = invoice_repository
        self._module_adapters = {
            "educacao": educacao_service,
            "juventude": juventude_service,
            "emprego": emprego_service,
            "saude": saude_service,
            "assistencia_social": assistencia_social_service,
            "service_requests": service_requests_service,
        }

    async def register_payment(self, data: CreatePaymentSchema) -> DomainPayment:
        if not self.payment_repo or not self.invoice_repo:
            raise NotImplementedError("register_payment requires repositories")

        if await self.payment_repo.exists_by_gateway_ref(data.gateway_reference):
            raise DuplicatePaymentError(data.gateway_reference)

        invoice = await self.invoice_repo.get_by_id(data.invoice_id)
        if not invoice:
            raise InvoiceNotFoundError(data.invoice_id)

        if round(float(data.amount), 2) != round(float(invoice.amount), 2):
            raise DomainValidationError("Montante do pagamento divergente do valor da fatura")

        if invoice.status == InvoiceStatus.PAID:
            raise InvalidInvoiceStateError(current_status=invoice.status.value, action="pagar novamente")
        if invoice.status == InvoiceStatus.CANCELLED:
            raise InvalidInvoiceStateError(
                current_status=invoice.status.value,
                action="processar pagamento",
            )

        payment = DomainPayment(
            id=str(uuid.uuid4()),
            invoice_id=data.invoice_id,
            citizen_id=data.citizen_id,
            amount=float(data.amount),
            currency=data.currency,
            gateway_reference=data.gateway_reference,
            payment_method=data.payment_method,
            status=PaymentStatus.COMPLETED,
            created_at=datetime.now(UTC),
            confirmed_at=datetime.now(UTC),
        )

        invoice.change_status(
            InvoiceStatus.PAID,
            reason=f"Liquidado via {data.payment_method} - Ref: {data.gateway_reference}",
        )
        new_payment = await self.payment_repo.create(payment)
        await self.invoice_repo.save(invoice)
        return new_payment

    async def get_payment_history(self, citizen_id: str) -> list[DomainPayment]:
        if not self.payment_repo:
            return []
        return await self.payment_repo.get_by_citizen(citizen_id)

    async def get_payment_by_reference(self, gateway_reference: str) -> DomainPayment | None:
        if self.payment_repo:
            return await self.payment_repo.get_by_gateway_ref(gateway_reference)
        return await self.get_by_reference(gateway_reference)

    async def list_payments_by_invoice(self, invoice_id: str) -> list[DomainPayment]:
        if not self.payment_repo:
            return []
        return await self.payment_repo.list_by_invoice(invoice_id)

    async def _generate_reference(self, prefix: str) -> str:
        return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"

    async def _get_latest_transaction(self, payment_id: int):
        result = await self.db.execute(("latest_transaction", payment_id))
        return result.scalars().first()

    @staticmethod
    def _is_valid_status_transition(current_status: PaymentStatus, new_status: PaymentStatus) -> bool:
        allowed = {
            PaymentStatus.PENDING: {
                PaymentStatus.PENDING,
                PaymentStatus.PROCESSING,
                PaymentStatus.CANCELLED,
                PaymentStatus.FAILED,
            },
            PaymentStatus.PROCESSING: {
                PaymentStatus.PROCESSING,
                PaymentStatus.COMPLETED,
                PaymentStatus.CANCELLED,
                PaymentStatus.FAILED,
            },
            PaymentStatus.COMPLETED: {
                PaymentStatus.COMPLETED,
                PaymentStatus.REFUNDED,
                PaymentStatus.PARTIALLY_REFUNDED,
            },
            PaymentStatus.PARTIALLY_REFUNDED: {
                PaymentStatus.PARTIALLY_REFUNDED,
                PaymentStatus.REFUNDED,
            },
            PaymentStatus.CANCELLED: {PaymentStatus.CANCELLED},
            PaymentStatus.FAILED: {PaymentStatus.FAILED},
            PaymentStatus.REFUNDED: {PaymentStatus.REFUNDED},
            PaymentStatus.RECONCILED: {PaymentStatus.RECONCILED},
            PaymentStatus.DISPUTED: {PaymentStatus.DISPUTED},
        }
        return new_status in allowed.get(current_status, {current_status})

    async def create_payment(self, payment_data: PaymentCreate, user_id: int):
        reference = await self._generate_reference("PAY")
        payment = Payment(
            amount=float(payment_data.amount),
            currency=payment_data.currency,
            method=payment_data.method,
            status=PaymentStatus.PENDING,
            reference=reference,
            description=payment_data.description,
            metadata_=payment_data.metadata,
        )
        transaction = PaymentTransaction(
            payment_id=payment.id,
            amount=float(payment_data.amount),
            currency=payment_data.currency,
            type=TransactionType.PAYMENT,
            status=TransactionStatus.PENDING,
            reference=reference,
            metadata_={"user_id": user_id},
        )
        self.db.add(payment)
        self.db.add(transaction)
        await self.db.commit()
        if hasattr(self.db, "refresh"):
            await self.db.refresh(payment)
        return payment

    async def get_payment(self, payment_id: int):
        result = await self.db.execute(("payment", payment_id))
        return result.scalars().first()

    async def get_by_reference(self, reference: str):
        result = await self.db.execute(("payment_reference", reference))
        return result.scalars().first()

    async def update_status(self, payment_id: int, status: PaymentStatus):
        return await self.update_payment_status(payment_id=payment_id, status=status)

    async def update_payment_status(
        self, payment_id: int, status: PaymentStatus, provider_reference: str | None = None
    ):
        payment = await self.get_payment(payment_id)
        if not payment:
            return None
        current_status = PaymentStatus(payment.status)
        if not self._is_valid_status_transition(current_status, status):
            raise ValueError("Invalid status transition")
        payment.status = status
        transaction = await self._get_latest_transaction(payment_id)
        if transaction:
            if status in {
                PaymentStatus.COMPLETED,
                PaymentStatus.REFUNDED,
                PaymentStatus.PARTIALLY_REFUNDED,
            }:
                transaction.status = TransactionStatus.COMPLETED
            elif status in {PaymentStatus.CANCELLED, PaymentStatus.FAILED}:
                transaction.status = TransactionStatus.FAILED
            else:
                transaction.status = TransactionStatus.PENDING
            if provider_reference:
                transaction.provider_reference = provider_reference
        await self.db.commit()
        return payment

    async def create_refund(
        self, payment_id: int, refund_data: RefundCreate, user_id: int
    ) -> RefundResponse:
        payment = await self.get_payment(payment_id)
        if not payment:
            return None
        if PaymentStatus(payment.status) != PaymentStatus.COMPLETED:
            raise ValueError("Can only refund completed payments")
        payment_amount = Decimal(str(payment.amount))
        refund_amount = (
            Decimal(str(refund_data.amount)) if refund_data.amount is not None else payment_amount
        )
        if refund_amount > payment_amount:
            raise ValueError("Refund amount cannot exceed payment amount")
        refund_reference = await self._generate_reference("RFD")
        transaction = PaymentTransaction(
            payment_id=payment.id,
            amount=float(refund_amount),
            currency=getattr(payment, "currency", "AOA"),
            type=TransactionType.REFUND,
            status=TransactionStatus.PENDING,
            reference=refund_reference,
            metadata_={"user_id": user_id, "reason": refund_data.reason},
        )
        self.db.add(transaction)
        payment.status = (
            PaymentStatus.REFUNDED
            if refund_amount == payment_amount
            else PaymentStatus.PARTIALLY_REFUNDED
        )
        await self.db.commit()
        return RefundResponse(
            amount=float(refund_amount),
            status=TransactionStatus.PENDING,
            reference=refund_reference,
        )

    async def delete_payment(self, payment_id: int, user_id: int) -> bool:
        payment = await self.get_payment(payment_id)
        if not payment:
            return False
        delete_result = self.db.delete(payment)
        if inspect.isawaitable(delete_result):
            await delete_result
        await self.db.commit()
        return True
