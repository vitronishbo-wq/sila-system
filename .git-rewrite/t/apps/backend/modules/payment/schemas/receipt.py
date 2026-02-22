"""Receipt schemas for request/response validation."""

from datetime import datetime
from typing import Optional, Dict, Any, List

from pydantic import BaseModel, ConfigDict, Field


class ReceiptLineItem(BaseModel):
    """Line item in a receipt."""

    description: str
    amount: float
    quantity: int = 1
    unit_price: float

    model_config = ConfigDict(from_attributes=True)


class ReceiptBase(BaseModel):
    """Base schema for receipt operations."""

    payment_id: int
    reference: str
    amount: float
    currency: str
    status: str
    method: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ReceiptResponse(ReceiptBase):
    """Receipt response schema."""

    id: int
    receipt_number: str
    line_items: List[ReceiptLineItem] = []
    subtotal: float
    tax: float = 0.0
    total: float
    payment_date: datetime
    issued_date: datetime
    due_date: Optional[datetime] = None
    notes: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)


class ReceiptPDFRequest(BaseModel):
    """Schema for requesting a PDF receipt."""

    payment_id: int = Field(..., description="Payment ID")
    include_qr_code: bool = Field(default=True, description="Include QR code in PDF")
    include_signature: bool = Field(default=False, description="Include signature line")
    language: str = Field(
        default="pt", regex="^(pt|en|es)$", description="Receipt language"
    )

    model_config = ConfigDict(from_attributes=True)


class ReceiptEmailRequest(BaseModel):
    """Schema for emailing a receipt."""

    payment_id: int = Field(..., description="Payment ID")
    email: str = Field(..., description="Email address to send receipt to")
    format: str = Field(default="pdf", regex="^(pdf|html)$", description="Email format")
    include_invoice: bool = Field(default=False, description="Include invoice in email")

    model_config = ConfigDict(from_attributes=True)
