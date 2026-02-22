"""Timeline schema"""
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any, List


class TimelineEventResponse(BaseModel):
    """Schema for timeline event"""
    type: str  # EVENT, ATTACHMENT, WORKFLOW
    timestamp: datetime
    actor_id: UUID
    event_type: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None
    filename: Optional[str] = None
    size_bytes: Optional[int] = None


class TimelineSummaryResponse(BaseModel):
    """Schema for timeline summary"""
    id: UUID
    status: str
    citizen_id: UUID
    service_type: str
    channel: str
    priority: str
    created_at: datetime
    updated_at: Optional[datetime]
    recent_events: List[Dict[str, Any]]
    attachments_count: int
    workflow_instance_id: Optional[str]
    
    model_config = ConfigDict(from_attributes=True)


class TimelineResponse(BaseModel):
    """Schema for full timeline"""
    request_id: UUID
    events: List[TimelineEventResponse]
    total: int
