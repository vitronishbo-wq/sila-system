"""Pydantic schemas for integration module CRUD operations."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class IntegrationEventType(str, Enum):
    """Types of integration events."""

    DATA_SYNC = "data_sync"
    USER_UPDATE = "user_update"
    NOTIFICATION = "notification"
    WORKFLOW_TRIGGER = "workflow_trigger"
    SYSTEM_EVENT = "system_event"
    API_CALL = "api_call"
    MESSAGE_QUEUE = "message_queue"


class IntegrationEventStatus(str, Enum):
    """Status of integration events."""

    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


# Base schema
class IntegrationEventBase(BaseModel):
    """Base schema for integration events."""

    event_id: str = Field(..., max_length=100)
    source_module: str = Field(..., max_length=50)
    target_module: str = Field(..., max_length=50)
    event_type: IntegrationEventType
    status: IntegrationEventStatus = IntegrationEventStatus.PENDING
    payload: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = Field(None, max_length=1000)
    retry_count: int = Field(default=0, ge=0)
    max_retries: int = Field(default=3, ge=0)


# Create schema
class IntegrationEventCreate(IntegrationEventBase):
    """Schema for creating an integration event."""


# Update schema
class IntegrationEventUpdate(BaseModel):
    """Schema for updating an integration event."""

    status: Optional[IntegrationEventStatus] = None
    payload: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = Field(None, max_length=1000)
    retry_count: Optional[int] = Field(None, ge=0)
    processed_at: Optional[datetime] = None


# Database schema (InDB)
class IntegrationEventInDB(IntegrationEventBase):
    """Schema for integration event as stored in database."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_by: int
    updated_by: Optional[int]
    created_at: datetime
    updated_at: datetime
    processed_at: Optional[datetime]


# Output schema (Out)
class IntegrationEventOut(IntegrationEventInDB):
    """Schema for integration event output (API response)."""


# Filter schema
class IntegrationEventFilter(BaseModel):
    """Schema for integration event filtering."""

    source_module: Optional[str] = Field(None, max_length=50)
    target_module: Optional[str] = Field(None, max_length=50)
    event_type: Optional[IntegrationEventType] = None
    status: Optional[IntegrationEventStatus] = None
    created_by: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None


# Batch operation schemas
class IntegrationEventBatchCreate(BaseModel):
    """Schema for batch creating integration events."""

    events: List[IntegrationEventCreate] = Field(..., min_items=1, max_items=100)


class IntegrationEventBatchUpdate(BaseModel):
    """Schema for batch updating integration events."""

    event_ids: List[int] = Field(..., min_items=1, max_items=100)
    update_data: IntegrationEventUpdate


# Statistics schema
class IntegrationEventStatistics(BaseModel):
    """Schema for integration event statistics."""

    total_events: int
    successful_events: int
    failed_events: int
    pending_events: int
