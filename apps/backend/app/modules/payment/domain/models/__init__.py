"""Modelos de domínio mínimos para o pacote de pagamentos."""

from dataclasses import dataclass, field
from datetime import UTC, datetime

from ..enums import InvoiceStatus, PaymentStatus


@dataclass
class Payment:
    """Entidade de domínio de pagamento usada pelos serviços e ports."""

    id: str
    invoice_id: str
    citizen_id: str
    amount: float
    gateway_reference: str
    payment_method: str
    currency: str = "AOA"
    status: PaymentStatus = PaymentStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    confirmed_at: datetime | None = None


@dataclass
class Invoice:
    """Entidade de domínio de fatura usada pelos serviços e ports."""

    id: str
    reference: str
    citizen_id: str
    amount: float
    service_code: str | None = None
    request_id: str | None = None
    status: InvoiceStatus = InvoiceStatus.DRAFT
    currency: str = "AOA"
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    issued_at: datetime | None = None
    due_at: datetime | None = None

    def change_status(self, new_status: InvoiceStatus, reason: str | None = None) -> dict[str, str]:
        self.status = new_status
        return {
            "entity_type": "INVOICE",
            "entity_id": self.id,
            "status": new_status.value,
            "reason": reason or "",
        }

    def is_payable(self) -> bool:
        return self.status in {InvoiceStatus.PENDING, InvoiceStatus.OVERDUE}


__all__ = ["Invoice", "Payment"]
