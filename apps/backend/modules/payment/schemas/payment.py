"""Payment schemas for request/response validation."""

from datetime import datetime
from typing import Any, Dict, Optional
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..models.enums import (
    PaymentMethod,
    PaymentStatus,
    TransactionStatus,
    TransactionType,
)


class PaymentBase(BaseModel):
    """Base schema for payment operations."""

    amount: float = Field(..., gt=0, description="Payment amount")
    currency: str = Field(
        default="AOA", max_length=3, description="Currency code (ISO 4217)"
    )
    method: PaymentMethod = Field(..., description="Payment method")
    description: Optional[str] = Field(
        None, max_length=255, description="Payment description"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional payment metadata",
    )

    @field_validator("metadata", mode="before")
    @classmethod
    def validate_metadata(cls, v):
        """Handle metadata pull from metadata_ or metadata."""
        if v is None:
            return None
        if isinstance(v, dict):
            return v
        # If it's an object (like ORM), check for metadata_ first to avoid SQLA metadata collision
        if hasattr(v, "metadata_"):
            return v.metadata_
        if hasattr(v, "metadata") and not isinstance(
            v.metadata, (dict, type(None))
        ):
            # Probably SQLA metadata, ignore it
            return None
        return getattr(v, "metadata", None)

    @field_validator("amount", mode="before")
    @classmethod
    def convert_amount(cls, v):
        """Convert Decimal or string to float."""
        if isinstance(v, Decimal):
            return float(v)
        if isinstance(v, str):
            return float(v)
        return v

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PaymentCreate(PaymentBase):
    """Schema for creating a new payment."""

    reference: Optional[str] = Field(
        None, max_length=100, description="Optional external reference ID"
    )
    due_date: Optional[str] = Field(
        None, description="Payment due date (YYYY-MM-DD, default: 30 days from now)"
    )
    payment_type: Optional[str] = Field(None, description="Payment type")


class PaymentUpdate(BaseModel):
    """Schema for updating a payment."""

    status: Optional[PaymentStatus] = None
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Additional payment metadata"
    )
    description: Optional[str] = Field(None, max_length=255)

    model_config = ConfigDict(populate_by_name=True)


class PaymentInDB(PaymentBase):
    """Payment schema for database operations."""

    id: int
    status: PaymentStatus
    reference: str
    created_at: datetime
    updated_at: datetime

    @field_validator("amount", mode="before")
    @classmethod
    def convert_amount(cls, v):
        """Convert Decimal or string to float."""
        if isinstance(v, Decimal):
            return float(v)
        if isinstance(v, str):
            return float(v)
        return v

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PaymentResponse(BaseModel):
    """Payment response schema."""

    id: int
    amount: Decimal
    currency: str
    status: PaymentStatus
    method: PaymentMethod
    reference: str
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Additional payment metadata"
    )
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    @field_validator("metadata", mode="before")
    @classmethod
    def validate_metadata(cls, v):
        """Handle metadata pull from metadata_ or metadata."""
        if v is None:
            return None
        if isinstance(v, dict):
            return v
        if hasattr(v, "metadata_"):
            return v.metadata_
        if hasattr(v, "metadata") and not isinstance(
            v.metadata, (dict, type(None))
        ):
            return None
        return getattr(v, "metadata", None)


class RefundCreate(BaseModel):
    """Schema for creating a refund."""

    amount: Optional[float] = Field(
        None,
        gt=0,
        description="Amount to refund. If not provided, full amount will be refunded",
    )
    reason: Optional[str] = Field(
        None, max_length=255, description="Reason for the refund"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Additional refund metadata"
    )

    model_config = ConfigDict(populate_by_name=True)


class RefundResponse(BaseModel):
    """Refund response schema."""

    id: int
    payment_id: int
    amount: Decimal
    currency: str
    status: TransactionStatus
    reference: str
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Additional refund metadata"
    )
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    @field_validator("metadata", mode="before")
    @classmethod
    def validate_metadata(cls, v):
        """Handle metadata pull from metadata_ or metadata."""
        if v is None:
            return None
        if isinstance(v, dict):
            return v
        if hasattr(v, "metadata_"):
            return v.metadata_
        if hasattr(v, "metadata") and not isinstance(
            v.metadata, (dict, type(None))
        ):
            return None
        return getattr(v, "metadata", None)


class TransactionResponse(BaseModel):
    """Transaction response schema."""

    id: int
    payment_id: int
    amount: float
    currency: str
    type: TransactionType
    status: TransactionStatus
    reference: str
    provider_reference: Optional[str]
    created_at: datetime

    @field_validator("amount", mode="before")
    @classmethod
    def convert_amount(cls, v):
        """Convert Decimal or string to float."""
        if isinstance(v, Decimal):
            return float(v)
        if isinstance(v, str):
            return float(v)
        return v

    model_config = ConfigDict(from_attributes=True)


class PaymentFilter(BaseModel):
    """Schema for filtering payments in queries."""

    status: Optional[PaymentStatus] = Field(
        None, description="Filter by payment status"
    )
    method: Optional[PaymentMethod] = Field(
        None, description="Filter by payment method"
    )
    date_from: Optional[str] = Field(
        None, description="Filter payments created after this date (YYYY-MM-DD)"
    )
    date_to: Optional[str] = Field(
        None, description="Filter payments created before this date (YYYY-MM-DD)"
    )
    min_amount: Optional[float] = Field(
        None, ge=0, description="Filter by minimum amount"
    )
    max_amount: Optional[float] = Field(
        None, ge=0, description="Filter by maximum amount"
    )
