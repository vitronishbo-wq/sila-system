"""Governance Request domain model."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from apps.backend.app.modules.governance.domain.models.enums import ApprovalLevel, RequestStatus


@dataclass
class GovernanceRequest:
    """Domain model for Governance Request."""

    id: str
    requester_id: str
    request_type: str
    description: str
    approval_level: ApprovalLevel
    status: RequestStatus = RequestStatus.PENDING
    approved_by: str | None = None
    rejection_reason: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    decided_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def approve(self, approver_id: str) -> dict[str, Any]:
        """Approve request."""
        old_status = self.status
        self.status = RequestStatus.APPROVED
        self.approved_by = approver_id
        self.decided_at = datetime.utcnow()
        self.updated_at = self.decided_at
        return {
            "entity_type": "GOVERNANCE_REQUEST",
            "entity_id": self.id,
            "action": "REQUEST_APPROVED",
            "previous_state": {"status": old_status.value},
            "new_state": {"status": self.status.value, "approved_by": approver_id},
            "timestamp": self.decided_at,
        }

    def reject(self, approver_id: str, reason: str = "") -> dict[str, Any]:
        """Reject request."""
        old_status = self.status
        self.status = RequestStatus.REJECTED
        self.approved_by = approver_id
        self.rejection_reason = reason
        self.decided_at = datetime.utcnow()
        self.updated_at = self.decided_at
        return {
            "entity_type": "GOVERNANCE_REQUEST",
            "entity_id": self.id,
            "action": "REQUEST_REJECTED",
            "previous_state": {"status": old_status.value},
            "new_state": {
                "status": self.status.value,
                "rejected_by": approver_id,
                "reason": reason,
            },
            "timestamp": self.decided_at,
        }

    def send_for_review(self) -> dict[str, Any]:
        """Send request for review."""
        old_status = self.status
        self.status = RequestStatus.IN_REVIEW
        self.updated_at = datetime.utcnow()
        return {
            "entity_type": "GOVERNANCE_REQUEST",
            "entity_id": self.id,
            "action": "REQUEST_SENT_FOR_REVIEW",
            "previous_state": {"status": old_status.value},
            "new_state": {"status": self.status.value},
            "timestamp": self.updated_at,
        }
