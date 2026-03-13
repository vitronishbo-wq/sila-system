from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from uuid import UUID
from datetime import date, datetime

class DebtBase(BaseModel):
    """Base model para dívida"""
    tax_type: str = Field(..., description='Tipo de imposto')
    original_amount: float = Field(..., gt=0, description='Valor original')
    due_date: date = Field(..., description='Data de vencimento')
    description: Optional[str] = Field(None, max_length=500)

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
    paid_at: Optional[datetime]
    status: str
    model_config = ConfigDict(from_attributes=True)

class DebtListResponse(BaseModel):
    """Schema para listagem de dívidas"""
    total: int
    items: List[DebtResponse]
    total_amount: float

class DebtPaymentRequest(BaseModel):
    """Schema para pagamento de dívida"""
    amount: float = Field(..., gt=0, description='Valor a pagar')
    payment_method: str = Field(..., description='Método de pagamento')
    reference: Optional[str] = None