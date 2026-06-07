from dataclasses import dataclass


@dataclass
class AuditEvent:
    event_id: str
    event_name: str
    hash: str
    previous_hash: str
