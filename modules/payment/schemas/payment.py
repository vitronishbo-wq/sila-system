from decimal import Decimal

from pydantic import BaseModel, Field

from modules.payment.models.enums import PaymentMethod, TransactionStatus


class PaymentCreate(BaseModel):
    amount: Decimal
    currency: str
    method: PaymentMethod
    description: str | None = None
    metadata: dict = Field(default_factory=dict)


class RefundCreate(BaseModel):
    amount: float | None = None
    reason: str


class RefundResponse(BaseModel):
    amount: float
    status: TransactionStatus
    reference: str
