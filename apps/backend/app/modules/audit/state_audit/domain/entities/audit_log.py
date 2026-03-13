from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from ..value_objects.audit_event_type import AuditEventType

@dataclass
class AuditLog:
    event_type: AuditEventType
    entity_id: UUID
    actor_id: UUID
    metadata: dict
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)