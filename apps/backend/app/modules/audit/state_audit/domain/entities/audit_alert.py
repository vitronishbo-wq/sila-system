from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from ..value_objects.audit_severity import AuditSeverity

@dataclass
class AuditAlert:
    rule_triggered: str
    entity_id: UUID
    severity: AuditSeverity
    description: str
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)