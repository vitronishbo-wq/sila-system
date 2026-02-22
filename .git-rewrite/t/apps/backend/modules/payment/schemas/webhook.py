"""Webhook schemas for request/response validation."""

from datetime import datetime
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class WebhookBase(BaseModel):
    """Base schema for webhook operations."""

    url: str = Field(..., description="Webhook URL")
    events: List[str] = Field(..., description="List of events to trigger webhook")
    active: bool = Field(default=True, description="Whether webhook is active")

    model_config = ConfigDict(from_attributes=True)


class WebhookCreate(WebhookBase):
    """Schema for creating a webhook."""

    secret_key: Optional[str] = Field(None, description="Secret key for HMAC signature")


class WebhookResponse(WebhookBase):
    """Webhook response schema."""

    id: int
    secret_key: Optional[str] = None
    retry_count: int
    last_triggered_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WebhookEventResponse(BaseModel):
    """Webhook event response schema."""

    id: int
    webhook_id: int
    payment_id: Optional[int] = None
    event_type: str
    payload: Dict[str, Any]
    delivered: bool
    delivery_attempts: int
    last_error: Optional[str] = None
    created_at: datetime
    delivered_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class WebhookTestRequest(BaseModel):
    """Schema for testing a webhook."""

    webhook_id: int = Field(..., description="Webhook ID to test")
    event_type: str = Field(default="payment.test", description="Test event type")
    payload: Optional[Dict[str, Any]] = Field(None, description="Custom test payload")

    model_config = ConfigDict(from_attributes=True)
