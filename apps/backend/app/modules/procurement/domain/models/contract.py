"""Procurement Contract domain model."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from apps.backend.app.modules.procurement.domain.models.enums import ContractStatus


@dataclass
class Contract:
    """Domain model for Procurement Contract."""

    id: str
    tender_id: str
    supplier_id: str
    amount: float
    start_date: datetime
    end_date: datetime
    status: ContractStatus = ContractStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)

    def complete(self) -> dict[str, Any]:
        """Mark contract as completed."""
        old_status = self.status
        self.status = ContractStatus.COMPLETED
        self.updated_at = datetime.utcnow()
        return {
            "entity_type": "CONTRACT",
            "entity_id": self.id,
            "action": "CONTRACT_COMPLETED",
            "previous_state": {"status": old_status.value},
            "new_state": {"status": self.status.value},
            "timestamp": self.updated_at,
        }

    def terminate(self, reason: str = "") -> dict[str, Any]:
        """Terminate contract early."""
        old_status = self.status
        self.status = ContractStatus.TERMINATED
        self.updated_at = datetime.utcnow()
        self.metadata["termination_reason"] = reason
        return {
            "entity_type": "CONTRACT",
            "entity_id": self.id,
            "action": "CONTRACT_TERMINATED",
            "previous_state": {"status": old_status.value},
            "new_state": {"status": self.status.value, "reason": reason},
            "timestamp": self.updated_at,
        }
