from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict


@dataclass
class TimeSeriesPoint:
    id: Optional[int]
    statistic_id: int
    value: float
    period_start: datetime
    period_end: Optional[datetime]
    dimensions: Optional[Dict]
    created_at: datetime
