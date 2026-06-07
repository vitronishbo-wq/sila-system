from datetime import datetime
from typing import Any

from pydantic import BaseModel


class TimeSeriesPointSchema(BaseModel):
    value: float
    period_start: datetime
    period_end: datetime | None = None
    dimensions: dict[str, Any] | None = None

    class Config:
        from_attributes = True


class TimeSeriesSchema(BaseModel):
    id: int
    statistic_id: int | None = None
    value: float
    period_start: str | None
    period_end: str | None
    dimensions: dict[str, Any] | None
    created_at: str | None = None

    class Config:
        from_attributes = True
