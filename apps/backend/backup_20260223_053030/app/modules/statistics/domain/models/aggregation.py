from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict


@dataclass
class Aggregation:
    id: Optional[int]
    statistic_id: int
    method: str
    parameters: Optional[Dict]
    created_at: datetime
