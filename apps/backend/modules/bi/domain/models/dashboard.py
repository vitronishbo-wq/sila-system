from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any


@dataclass
class Dashboard:
    id: Optional[int]
    name: str
    description: Optional[str]
    owner_id: Optional[int]
    layout: Optional[Any]
    created_at: datetime
