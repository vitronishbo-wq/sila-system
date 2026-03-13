from dataclasses import dataclass

from modules.payment.models.enums import PaymentStatus


@dataclass
class Payment:
    id: int
    reference: str
    status: PaymentStatus = PaymentStatus.PENDING
