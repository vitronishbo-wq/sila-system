from dataclasses import dataclass
from uuid import UUID

@dataclass
class SubmitBid:
    tender_id: UUID
    supplier_id: UUID
    amount: float