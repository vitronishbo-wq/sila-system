from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Statistic:
    id: Optional[int]
    name: str
    code: str
    description: Optional[str]
    unit: Optional[str]
    source_module: Optional[str]
    created_at: datetime