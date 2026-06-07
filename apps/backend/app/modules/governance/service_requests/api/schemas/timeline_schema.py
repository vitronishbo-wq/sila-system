"""Timeline schema"""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TimelineEventResponse(BaseModel):
    """Schema for timeline event"""

    type: str
    timestamp: datetime
    actor_id: UUID
    event_type: str | None = None
    payload: dict[str, Any] | None = None
    filename: str | None = None
    size_bytes: int | None = None


class TimelineSummaryResponse(BaseModel):
    """Schema for timeline summary"""

    id: UUID
    status: str
    citizen_id: UUID
    service_type: str
    channel: str
    priority: str
    created_at: datetime
    updated_at: datetime | None
    recent_events: list[dict[str, Any]]
    attachments_count: int
    workflow_instance_id: str | None
    model_config = ConfigDict(from_attributes=True)


class TimelineResponse(BaseModel):
    """Schema for full timeline"""

    request_id: UUID
    events: list[TimelineEventResponse]
    total: int
