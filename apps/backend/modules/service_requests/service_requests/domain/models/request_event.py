"""Request event domain model"""
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, Dict, Any


@dataclass
class RequestEvent:
    """Request event for audit trail and timeline"""
    request_id: UUID = field()
    event_type: str = field()  # CREATED, WORKFLOW_STARTED, STATE_CHANGED, ATTACHMENT_ADDED, CLOSED
    actor_id: UUID = field()
    id: UUID = field(default_factory=uuid4)
    payload: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "request_id": str(self.request_id),
            "event_type": self.event_type,
            "payload": self.payload,
            "actor_id": str(self.actor_id),
            "created_at": self.created_at.isoformat(),
        }
