from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4
from typing import Optional

@dataclass
class TaxpayerDebt:
    id: UUID = field(default_factory=uuid4)
    taxpayer_id: UUID = field(default_factory=uuid4)
    amount: float = 0.0
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: str = 'open'
    created_at: Optional[date] = None