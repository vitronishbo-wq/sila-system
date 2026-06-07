from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Bid:
    tender_id: UUID
    supplier_id: UUID
    amount: float
    id: UUID = field(default_factory=uuid4)
    submitted_at: datetime = field(default_factory=datetime.utcnow)
