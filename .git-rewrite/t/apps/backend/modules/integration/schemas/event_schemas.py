# auto-generated placeholder
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict


class EventBase(BaseModel):
    event_type: str
    source_module: str
    payload: Optional[Dict[str, Any]] = None


class EventCreate(EventBase):
    pass


class EventResponse(EventBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(orm_mode=True)


class EventFilter(BaseModel):
    event_type: Optional[str] = None
    source_module: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = 100
