from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DebtBase(BaseModel):
    """Base model para dívida"""

    tax_type: str = Field(..., description="Tipo de imposto")
    original_amount: float = Field(..., gt=0, description="Valor original")
    due_date: date = Field(..., description="Data de vencimento")
    description: str | None = Field(None, max_length=500)


class DebtCreate(DebtBase):
    """Schema para criação de dívida"""

    pass


class DebtResponse(DebtBase):
    """Schema para resposta de dívida"""

    id: UUID
    taxpayer_id: UUID
    debt_number: str
    current_amount: float
    interest: float
    fines: float
    created_date: date
    paid_at: datetime | None
    status: str
    model_config = ConfigDict(from_attributes=True)


class DebtListResponse(BaseModel):
    """Schema para listagem de dívidas"""

    total: int
    items: list[DebtResponse]
    total_amount: float


class DebtPaymentRequest(BaseModel):
    """Schema para pagamento de dívida"""

    amount: float = Field(..., gt=0, description="Valor a pagar")
    payment_method: str = Field(..., description="Método de pagamento")
    reference: str | None = None
