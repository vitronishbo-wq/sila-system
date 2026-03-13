from __future__ import annotations

from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field

from apps.backend.app.modules.payment.models.enums import PaymentMethod, TransactionStatus


class PaymentCreate(BaseModel):
    amount: Decimal
    currency: str = "AOA"
    method: PaymentMethod
    description: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class RefundCreate(BaseModel):
    amount: float | None = None
    reason: str | None = None


class RefundResponse(BaseModel):
    amount: float
    status: TransactionStatus
    reference: str
