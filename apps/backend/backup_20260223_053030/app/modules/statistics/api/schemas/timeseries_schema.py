from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class TimeSeriesPointSchema(BaseModel):
    value: float
    period_start: datetime
    period_end: Optional[datetime] = None
    dimensions: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


class TimeSeriesSchema(BaseModel):
    id: int
    statistic_id: Optional[int] = None
    value: float
    period_start: Optional[str]
    period_end: Optional[str]
    dimensions: Optional[Dict[str, Any]]
    created_at: Optional[str] = None

    class Config:
        from_attributes = True

