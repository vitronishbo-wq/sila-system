"""Procurement Supplier domain model."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Supplier:
    """Domain model for Procurement Supplier."""

    id: str
    name: str
    tax_id: str
    contact: str
    status: str = "ACTIVE"
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)

    def deactivate(self, reason: str = "") -> dict[str, Any]:
        """Deactivate supplier."""
        old_status = self.status
        self.status = "INACTIVE"
        self.updated_at = datetime.utcnow()
        self.metadata["deactivation_reason"] = reason
        return {
            "entity_type": "SUPPLIER",
            "entity_id": self.id,
            "action": "SUPPLIER_DEACTIVATED",
            "previous_state": {"status": old_status},
            "new_state": {"status": self.status},
            "timestamp": self.updated_at,
        }
