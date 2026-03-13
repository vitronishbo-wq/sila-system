from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from ..value_objects.contract_status import ContractStatus

@dataclass
class Contract:
    tender_id: UUID
    supplier_id: UUID
    value: float
    id: UUID = field(default_factory=uuid4)
    status: ContractStatus = ContractStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.utcnow)