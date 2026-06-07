from dataclasses import dataclass
from datetime import datetime


@dataclass
class Statistic:
    id: int | None
    name: str
    code: str
    description: str | None
    unit: str | None
    source_module: str | None
    created_at: datetime
