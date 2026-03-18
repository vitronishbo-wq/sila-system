"""Pydantic schemas para API de Pagamentos."""
from typing import Any, Optional
from decimal import Decimal

from pydantic import BaseModel, Field

from ...domain.enums import PaymentMethod, PaymentStatus, TransactionStatus


class CreatePaymentSchema(BaseModel):
    """Schema para registar um novo pagamento."""
    invoice_id: str = Field(..., description="ID da Fatura")
    citizen_id: str = Field(..., description="ID do Cidadão")
    amount: float = Field(..., gt=0, description="Montante do pagamento")
    currency: str = Field(default="AOA", description="Moeda (ISO 4217)")
    gateway_reference: str = Field(
        ..., 
        description="Referência de gateway de pagamento (chave de idempotência)"
    )
    payment_method: str = Field(..., description="Método de pagamento")

    class Config:
        schema_extra = {
            "example": {
                "invoice_id": "INV-001-2026",
                "citizen_id": "12345678901AB",
                "amount": 5000.0,
                "currency": "AOA",
                "gateway_reference": "GW-PAY-2026-031201",
                "payment_method": "credit_card",
            }
        }


class PaymentResponse(BaseModel):
    """Schema para resposta de pagamento processado."""
    id: str = Field(..., description="ID do Pagamento")
    invoice_id: str = Field(..., description="ID da Fatura")
    citizen_id: str = Field(..., description="ID do Cidadão")
    amount: float = Field(..., description="Montante")
    currency: str = Field(..., description="Moeda")
    gateway_reference: str = Field(..., description="Referência de gateway")
    payment_method: str = Field(..., description="Método de pagamento")
    status: str = Field(..., description="Estado do pagamento")
    created_at: str = Field(..., description="Data de criação")
    confirmed_at: Optional[str] = Field(None, description="Data de confirmação")

    class Config:
        schema_extra = {
            "example": {
                "id": "57f2e1a0-1234-5678-9abc-def012345678",
                "invoice_id": "INV-001-2026",
                "citizen_id": "12345678901AB",
                "amount": 5000.0,
                "currency": "AOA",
                "gateway_reference": "GW-PAY-2026-031201",
                "payment_method": "credit_card",
                "status": "completed",
                "created_at": "2026-03-17T10:30:00Z",
                "confirmed_at": "2026-03-17T10:30:05Z",
            }
        }


class PaymentHistoryResponse(BaseModel):
    """Schema para histórico de pagamentos de um cidadão."""
    total_count: int = Field(..., description="Total de pagamentos")
    payments: list[PaymentResponse] = Field(..., description="Lista de pagamentos")


# Legacy schemas para compatibilidade
class PaymentCreate(BaseModel):
    """Schema legado para criar pagamento."""
    amount: float
    currency: str = "AOA"
    method: str
    description: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class RefundCreate(BaseModel):
    """Schema para criar reembolso."""
    amount: Optional[float] = None
    reason: Optional[str] = None


class RefundResponse(BaseModel):
    """Schema para resposta de reembolso."""
    amount: float
    status: str
    reference: str


__all__ = [
    "CreatePaymentSchema",
    "PaymentResponse",
    "PaymentHistoryResponse",
    "PaymentCreate",
    "RefundCreate",
    "RefundResponse",
]
