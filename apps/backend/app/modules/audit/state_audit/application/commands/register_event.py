from dataclasses import dataclass
from uuid import UUID


@dataclass
class RegisterEvent:
    event_type: str
    entity_id: UUID
    actor_id: UUID
    metadata: dict
