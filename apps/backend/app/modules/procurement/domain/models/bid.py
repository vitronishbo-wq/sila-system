"""Procurement Bid domain model."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from apps.backend.app.modules.procurement.domain.models.enums import BidStatus

@dataclass
class Bid:
    """Domain model for Supplier Bid."""
    id: str
    tender_id: str
    supplier_id: str
    amount: float
    proposal: str
    status: BidStatus = BidStatus.SUBMITTED
    submitted_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    evaluated_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def evaluate(self, accepted: bool, reason: str='') -> Dict[str, Any]:
        """Evaluate bid submission."""
        old_status = self.status
        self.status = BidStatus.ACCEPTED if accepted else BidStatus.REJECTED
        self.evaluated_at = datetime.utcnow()
        self.updated_at = self.evaluated_at
        self.metadata['evaluation_reason'] = reason
        return {'entity_type': 'BID', 'entity_id': self.id, 'action': 'BID_EVALUATED', 'previous_state': {'status': old_status.value}, 'new_state': {'status': self.status.value, 'reason': reason}, 'timestamp': self.evaluated_at}