from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class AuditCase:
    title: str
    description: str
    entity_id: UUID
    id: UUID = field(default_factory=uuid4)
    opened_at: datetime = field(default_factory=datetime.utcnow)
    resolved: bool = False
