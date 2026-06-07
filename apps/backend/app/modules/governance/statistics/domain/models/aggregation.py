from dataclasses import dataclass
from datetime import datetime


@dataclass
class Aggregation:
    id: int | None
    statistic_id: int
    method: str
    parameters: dict | None
    created_at: datetime
