"""Procurement Tender domain model."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from apps.backend.app.modules.procurement.domain.models.enums import TenderStatus


@dataclass
class Tender:
    """Domain model for public Tender."""

    id: str
    title: str
    description: str
    budget: float
    deadline: datetime
    status: TenderStatus = TenderStatus.OPEN
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    awarded_to: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def close(self) -> dict[str, Any]:
        """Close tender for new bids."""
        old_status = self.status
        self.status = TenderStatus.CLOSED
        self.updated_at = datetime.utcnow()
        return {
            "entity_type": "TENDER",
            "entity_id": self.id,
            "action": "TENDER_CLOSED",
            "previous_state": {"status": old_status.value},
            "new_state": {"status": self.status.value},
            "timestamp": self.updated_at,
        }

    def award(self, supplier_id: str) -> dict[str, Any]:
        """Award tender to supplier."""
        old_status = self.status
        old_awarded = self.awarded_to
        self.status = TenderStatus.AWARDED
        self.awarded_to = supplier_id
        self.updated_at = datetime.utcnow()
        return {
            "entity_type": "TENDER",
            "entity_id": self.id,
            "action": "TENDER_AWARDED",
            "previous_state": {"status": old_status.value, "awarded_to": old_awarded},
            "new_state": {"status": self.status.value, "awarded_to": supplier_id},
            "timestamp": self.updated_at,
        }
