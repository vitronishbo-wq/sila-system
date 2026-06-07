from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4


@dataclass
class BilheteIdentidade:
    citizen_id: UUID
    number: str
    issued_at: date
    expires_at: date
    id: UUID = field(default_factory=uuid4)
