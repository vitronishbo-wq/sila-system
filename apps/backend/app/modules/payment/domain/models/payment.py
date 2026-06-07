from dataclasses import dataclass

from apps.backend.app.modules.payment.domain.enums import PaymentStatus


@dataclass
class Payment:
    id: int
    reference: str
    status: PaymentStatus = PaymentStatus.PENDING
