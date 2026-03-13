from dataclasses import dataclass
from uuid import UUID

@dataclass
class Bovino:
    animal_id: UUID
    aptidao: str | None = None