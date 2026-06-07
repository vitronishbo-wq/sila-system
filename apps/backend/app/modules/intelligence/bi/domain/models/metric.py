from dataclasses import dataclass
from datetime import datetime


@dataclass
class Metric:
    id: int | None
    name: str
    code: str
    value: float
    source: str
    dimension: str
    period: str
    created_at: datetime
