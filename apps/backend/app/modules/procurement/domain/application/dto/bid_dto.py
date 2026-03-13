from dataclasses import dataclass

@dataclass
class BidDTO:
    id: str
    tender_id: str
    supplier_id: str
    amount: float