from dataclasses import dataclass
from datetime import datetime


@dataclass
class Report:
    id: int | None
    name: str
    query: str
    parameters: dict | None
    created_by: int | None
    created_at: datetime
