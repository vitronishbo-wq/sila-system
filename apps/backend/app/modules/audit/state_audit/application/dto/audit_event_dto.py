from dataclasses import dataclass


@dataclass
class AuditEventDTO:
    type: str
    entity_id: str
    actor_id: str
    metadata: dict
