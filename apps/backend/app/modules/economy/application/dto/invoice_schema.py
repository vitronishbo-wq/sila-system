"""
Pydantic schemas for Invoice API.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class CreateInvoiceSchema(BaseModel):
    """Schema for creating a new invoice."""

    citizen_id: str = Field(..., description="Citizen ID (national ID)")
    service_code: str = Field(..., description="Service code")
    service_name: str = Field(..., description="Service name")
    revenue_code: str = Field(..., description="Revenue code")
    cost_center: str = Field(..., description="Cost center")
    amount: float = Field(..., gt=0, description="Invoice amount")
    due_date: datetime = Field(..., description="Due date")
    currency: str = Field(default="AOA", description="Currency (ISO 4217)")
    request_id: str | None = Field(None, description="Optional request ID")

    class Config:
        json_schema_extra = {
            "example": {
                "citizen_id": "12345678901AB",
                "service_code": "EDU_PROPINA",
                "service_name": "School Tuition",
                "revenue_code": "4211.08.01",
                "cost_center": "CC001",
                "amount": 5000.0,
                "due_date": "2026-04-12T23:59:59",
                "currency": "AOA",
                "request_id": "REQ-123456",
            }
        }
