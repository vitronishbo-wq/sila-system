from dataclasses import dataclass
from uuid import UUID

@dataclass
class OpenAuditCase:
    title: str
    description: str
    entity_id: UUID