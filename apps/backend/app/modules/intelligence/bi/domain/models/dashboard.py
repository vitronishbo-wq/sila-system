from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Dashboard:
    id: int | None
    name: str
    description: str | None
    owner_id: int | None
    layout: Any | None
    created_at: datetime
