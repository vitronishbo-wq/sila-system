"""Governance Workflow domain model."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from apps.backend.app.modules.governance.domain.models.enums import WorkflowStatus

@dataclass
class Workflow:
    """Domain model for Governance Workflow."""
    id: str
    process_name: str
    status: WorkflowStatus = WorkflowStatus.DRAFT
    current_step: int = 0
    total_steps: int = 1
    owner_id: str = ''
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    steps_history: List[Dict[str, Any]] = field(default_factory=list)

    def start(self) -> Dict[str, Any]:
        """Start workflow."""
        old_status = self.status
        self.status = WorkflowStatus.IN_PROGRESS
        self.updated_at = datetime.utcnow()
        return {'entity_type': 'WORKFLOW', 'entity_id': self.id, 'action': 'WORKFLOW_STARTED', 'previous_state': {'status': old_status.value}, 'new_state': {'status': self.status.value}, 'timestamp': self.updated_at}

    def transition(self, next_step: int) -> Dict[str, Any]:
        """Transition to next step."""
        old_step = self.current_step
        self.current_step = next_step
        self.updated_at = datetime.utcnow()
        self.steps_history.append({'step': next_step, 'transitioned_at': self.updated_at.isoformat()})
        return {'entity_type': 'WORKFLOW', 'entity_id': self.id, 'action': 'WORKFLOW_TRANSITIONED', 'previous_state': {'step': old_step}, 'new_state': {'step': next_step}, 'timestamp': self.updated_at}

    def complete(self) -> Dict[str, Any]:
        """Mark workflow as completed."""
        old_status = self.status
        self.status = WorkflowStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        self.updated_at = self.completed_at
        return {'entity_type': 'WORKFLOW', 'entity_id': self.id, 'action': 'WORKFLOW_COMPLETED', 'previous_state': {'status': old_status.value}, 'new_state': {'status': self.status.value}, 'timestamp': self.completed_at}

    def cancel(self, reason: str='') -> Dict[str, Any]:
        """Cancel workflow."""
        old_status = self.status
        self.status = WorkflowStatus.CANCELLED
        self.updated_at = datetime.utcnow()
        self.metadata['cancellation_reason'] = reason
        return {'entity_type': 'WORKFLOW', 'entity_id': self.id, 'action': 'WORKFLOW_CANCELLED', 'previous_state': {'status': old_status.value}, 'new_state': {'status': self.status.value, 'reason': reason}, 'timestamp': self.updated_at}