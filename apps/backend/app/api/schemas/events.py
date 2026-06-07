"""
Pydantic schemas for Event API responses.
Defines the contract for event-related API endpoints.
"""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class EventMetadata(BaseModel):
    """Metadata associated with an event."""

    correlation_id: UUID | None = None
    causation_id: UUID | None = None
    user_id: str | None = None
    request_id: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
                "causation_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
                "user_id": "user-123",
                "request_id": "req-456",
            }
        }


class EventResponse(BaseModel):
    """Event response model for API responses."""

    event_id: UUID = Field(..., description="Unique event identifier")
    aggregate_id: UUID = Field(..., description="ID of the aggregate that produced this event")
    aggregate_type: str = Field(..., description="Type of the aggregate (e.g., Citizen, Payment)")
    event_type: str = Field(
        ..., description="Type of event (e.g., CitizenCreated, PaymentProcessed)"
    )
    version: int = Field(default=1, description="Event version for schema evolution")
    timestamp: datetime = Field(..., description="When the event occurred (UTC)")
    event_data: dict[str, Any] = Field(default_factory=dict, description="Event payload data")
    metadata: dict[str, Any] | None = Field(default=None, description="Additional metadata")
    created_at: datetime | None = Field(None, description="When the event was persisted")

    class Config:
        json_schema_extra = {
            "example": {
                "event_id": "550e8400-e29b-41d4-a716-446655440000",
                "aggregate_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
                "aggregate_type": "Citizen",
                "event_type": "CitizenCreated",
                "version": 1,
                "timestamp": "2026-03-14T17:00:00Z",
                "event_data": {
                    "first_name": "João",
                    "last_name": "Silva",
                    "birth_date": "1990-01-15",
                },
                "metadata": None,
                "created_at": "2026-03-14T17:00:00Z",
            }
        }


class EventListResponse(BaseModel):
    """Paginated event list response."""

    events: list[EventResponse] = Field(default_factory=list, description="List of events")
    total: int = Field(default=0, description="Total number of events")
    limit: int = Field(default=100, description="Limit of events per page")
    offset: int = Field(default=0, description="Offset for pagination")

    class Config:
        json_schema_extra = {
            "example": {
                "events": [
                    {
                        "event_id": "550e8400-e29b-41d4-a716-446655440000",
                        "aggregate_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
                        "aggregate_type": "Citizen",
                        "event_type": "CitizenCreated",
                        "version": 1,
                        "timestamp": "2026-03-14T17:00:00Z",
                        "event_data": {},
                        "metadata": None,
                        "created_at": "2026-03-14T17:00:00Z",
                    }
                ],
                "total": 150,
                "limit": 100,
                "offset": 0,
            }
        }


class EventStreamResponse(BaseModel):
    """Event stream for an aggregate."""

    aggregate_id: UUID = Field(..., description="The aggregate ID")
    aggregate_type: str = Field(..., description="The aggregate type")
    events: list[EventResponse] = Field(default_factory=list, description="Event stream")
    event_count: int = Field(default=0, description="Number of events in stream")

    class Config:
        json_schema_extra = {
            "example": {
                "aggregate_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
                "aggregate_type": "Citizen",
                "events": [],
                "event_count": 0,
            }
        }


class HealthCheckResponse(BaseModel):
    """Health check response for event store."""

    status: str = Field(..., description="Health status (healthy/unhealthy)")
    event_store_type: str = Field(..., description="Type of event store (memory/postgres)")
    message: str = Field(..., description="Status message")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "event_store_type": "postgres",
                "message": "Event store is operational",
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""

    detail: str = Field(..., description="Error description")
    error_code: str | None = Field(None, description="Internal error code")

    class Config:
        json_schema_extra = {
            "example": {"detail": "Event not found", "error_code": "EVENT_NOT_FOUND"}
        }
