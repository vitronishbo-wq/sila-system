"""Identity domain model."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from apps.backend.app.modules.identity.domain.models.enums import IdentityStatus, TrustLevel


@dataclass
class Identity:
    """Domain model for Citizen Identity."""

    id: str
    citizen_id: str
    document_id: str
    full_name: str
    status: IdentityStatus = IdentityStatus.PENDING
    trust_level: TrustLevel = TrustLevel.LOW
    verified_at: datetime | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)

    def verify(self) -> dict[str, Any]:
        """Mark identity as verified."""
        old_status = self.status
        self.status = IdentityStatus.VERIFIED
        self.verified_at = datetime.utcnow()
        self.updated_at = self.verified_at
        return {
            "entity_type": "IDENTITY",
            "entity_id": self.id,
            "action": "IDENTITY_VERIFIED",
            "previous_state": {"status": old_status.value},
            "new_state": {"status": self.status.value},
            "timestamp": self.verified_at,
        }

    def reject(self, reason: str = "") -> dict[str, Any]:
        """Mark identity as rejected."""
        old_status = self.status
        self.status = IdentityStatus.REJECTED
        self.updated_at = datetime.utcnow()
        self.metadata["rejection_reason"] = reason
        return {
            "entity_type": "IDENTITY",
            "entity_id": self.id,
            "action": "IDENTITY_REJECTED",
            "previous_state": {"status": old_status.value},
            "new_state": {"status": self.status.value, "reason": reason},
            "timestamp": self.updated_at,
        }
