from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict


@dataclass
class Report:
    id: Optional[int]
    name: str
    query: str
    parameters: Optional[Dict]
    created_by: Optional[int]
    created_at: datetime
