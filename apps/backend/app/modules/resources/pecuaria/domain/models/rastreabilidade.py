from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Rastreabilidade:
    id: UUID
    animal_id: UUID
    evento: str
    timestamp: datetime

    @classmethod
    def registrar(cls, *, animal_id: UUID, evento: str) -> "Rastreabilidade":
        return cls(id=uuid4(), animal_id=animal_id, evento=evento, timestamp=datetime.utcnow())
