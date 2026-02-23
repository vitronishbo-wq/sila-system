from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Metric:
    id: Optional[int]
    name: str
    code: str
    value: float
    source: str
    dimension: str
    period: str
    created_at: datetime
