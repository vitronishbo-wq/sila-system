from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from typing import Optional
import re
from app.modules.financas.domain.models.enums import PaymentStatus

class PaymentBase(BaseModel):
    """Atributos fundamentais de uma transação financeira."""
    invoice_id: str = Field(..., description="UUID da fatura associada")
    citizen_id: str = Field(..., description="Identificador do pagador")
    amount: float = Field(..., gt=0, description="Valor transacionado")
    currency: str = Field(default="AOA", description="Moeda da transação")
    payment_method: str = Field(
        ..., 
        description="Canal de pagamento",
        examples=["MULTICAIXA_EXPRESS", "CASH", "BANK_TRANSFER"]
    )

    @field_validator('currency')
    @classmethod
    def validate_currency(cls, v: str) -> str:
        v = v.strip().upper()
        if not re.match(r'^[A-Z]{3}$', v):
            raise ValueError("Moeda inválida (ISO 4217 exigido)")
        return v

class CreatePaymentSchema(PaymentBase):
    """Schema para registro inicial de um pagamento."""
    gateway_reference: str = Field(
        ..., 
        description="Referência única externa do provedor de pagamento"
    )

class UpdatePaymentSchema(BaseModel):
    """Schema para atualizações de estado do pagamento (Reconciliação)."""
    status: Optional[PaymentStatus] = None
    confirmed_at: Optional[datetime] = None
    gateway_reference: Optional[str] = None

class PaymentResponse(PaymentBase):
    """Schema de resposta completo para auditoria e histórico."""
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    gateway_reference: str
    status: PaymentStatus
    created_at: datetime
    confirmed_at: Optional[datetime] = None
