from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from uuid import UUID, uuid4
from ..value_objects.procurement_method import ProcurementMethod
from ..value_objects.tender_status import TenderStatus

@dataclass
class Tender:
    title: str
    description: str
    budget_program_id: UUID
    estimated_value: float
    method: ProcurementMethod
    id: UUID = field(default_factory=uuid4)
    status: TenderStatus = TenderStatus.DRAFT
    created_at: datetime = field(default_factory=datetime.utcnow)
    bids: List['Bid'] = field(default_factory=list)

    def open(self) -> None:
        if self.status != TenderStatus.DRAFT:
            raise ValueError('Tender cannot be opened')
        self.status = TenderStatus.OPEN

    def close(self) -> None:
        if self.status != TenderStatus.OPEN:
            raise ValueError('Tender cannot be closed')
        self.status = TenderStatus.EVALUATION

    def add_bid(self, bid: 'Bid') -> None:
        if self.status != TenderStatus.OPEN:
            raise ValueError('Tender not open')
        self.bids.append(bid)