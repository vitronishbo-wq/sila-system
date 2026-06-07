from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4


@dataclass
class TaxpayerDebt:
    id: UUID = field(default_factory=uuid4)
    taxpayer_id: UUID = field(default_factory=uuid4)
    amount: float = 0.0
    description: str | None = None
    due_date: date | None = None
    status: str = "open"
    created_at: date | None = None
