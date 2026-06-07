from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SyncLogResponse(BaseModel):
    id: uuid.UUID
    entity_type: str
    entity_id: str
    direction: str
    status: str
    payload: Optional[dict] = None
    response: Optional[dict] = None
    error: Optional[str] = None
    duration_ms: int = 0
    retry_count: int = 0
    next_retry_at: Optional[datetime] = None
    created_at: datetime


class SyncStatsResponse(BaseModel):
    total_synced: int = 0
    success_count: int = 0
    failed_count: int = 0
    retry_count: int = 0
    dead_letter_count: int = 0
    pending_count: int = 0
    last_sync_at: Optional[datetime] = None


class TriggerSyncRequest(BaseModel):
    entity_type: str = Field(default="enrollment", description="Entity type to sync")
    entity_ids: Optional[list[str]] = Field(default=None, description="Specific entity IDs (sync all if None)")
    direction: str = Field(default="push", description="push or pull")


class TriggerSyncResponse(BaseModel):
    triggered: bool
    entity_type: str
    count: int
    message: str
