"""Compliance Check domain model."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from apps.backend.app.modules.compliance.domain.models.enums import ComplianceStatus

@dataclass
class ComplianceCheck:
    """Domain model for Compliance Check."""
    id: str
    rule_id: str
    entity_type: str
    entity_id: str
    status: ComplianceStatus = ComplianceStatus.PENDING
    result: str = ''
    checked_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def pass_check(self, message: str='') -> Dict[str, Any]:
        """Mark compliance check as passed."""
        old_status = self.status
        self.status = ComplianceStatus.PASSED
        self.result = message
        self.checked_at = datetime.utcnow()
        self.updated_at = self.checked_at
        return {'entity_type': 'COMPLIANCE_CHECK', 'entity_id': self.id, 'action': 'COMPLIANCE_PASSED', 'previous_state': {'status': old_status.value}, 'new_state': {'status': self.status.value, 'result': message}, 'timestamp': self.checked_at}

    def fail_check(self, reason: str='') -> Dict[str, Any]:
        """Mark compliance check as failed."""
        old_status = self.status
        self.status = ComplianceStatus.FAILED
        self.result = reason
        self.checked_at = datetime.utcnow()
        self.updated_at = self.checked_at
        return {'entity_type': 'COMPLIANCE_CHECK', 'entity_id': self.id, 'action': 'COMPLIANCE_FAILED', 'previous_state': {'status': old_status.value}, 'new_state': {'status': self.status.value, 'reason': reason}, 'timestamp': self.checked_at}