from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PaymentBase(BaseModel):
    """Base model para pagamento"""

    amount: float = Field(..., gt=0, description="Valor do pagamento")
    payment_method: str = Field(..., description="Método de pagamento")
    reference: str | None = Field(None, description="Referência externa")


class PaymentCreate(PaymentBase):
    """Schema para criação de pagamento"""

    debt_ids: list[UUID] = Field(..., description="IDs das dívidas a pagar")


class PaymentResponse(PaymentBase):
    """Schema para resposta de pagamento"""

    id: UUID
    taxpayer_id: UUID
    debt_id: UUID
    payment_number: str
    payment_date: datetime
    status: str
    paid_by: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class PaymentListResponse(BaseModel):
    """Schema para listagem de pagamentos"""

    total: int
    items: list[PaymentResponse]
    total_amount: float


class PaymentReverseRequest(BaseModel):
    """Schema para estorno de pagamento"""

    reason: str = Field(..., min_length=5, max_length=500, description="Motivo do estorno")
