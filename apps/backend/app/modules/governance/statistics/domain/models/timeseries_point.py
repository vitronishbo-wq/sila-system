from dataclasses import dataclass
from datetime import datetime


@dataclass
class TimeSeriesPoint:
    id: int | None
    statistic_id: int
    value: float
    period_start: datetime
    period_end: datetime | None
    dimensions: dict | None
    created_at: datetime
