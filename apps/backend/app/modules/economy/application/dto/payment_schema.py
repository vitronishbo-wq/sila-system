"""
Pydantic schemas for Payment API.
"""

from pydantic import BaseModel, Field


class CreatePaymentSchema(BaseModel):
    """Schema for registering a new payment."""

    invoice_id: str = Field(..., description="Invoice ID")
    citizen_id: str = Field(..., description="Citizen ID")
    amount: float = Field(..., gt=0, description="Payment amount")
    currency: str = Field(default="AOA", description="Currency (ISO 4217)")
    gateway_reference: str = Field(..., description="Payment gateway reference (idempotency key)")
    payment_method: str = Field(..., description="Payment method (e.g., card, transfer)")

    class Config:
        json_schema_extra = {
            "example": {
                "invoice_id": "INV-001-2026",
                "citizen_id": "12345678901AB",
                "amount": 5000.0,
                "currency": "AOA",
                "gateway_reference": "GW-PAY-2026-031201",
                "payment_method": "credit_card",
            }
        }
