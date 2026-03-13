from dataclasses import dataclass
from uuid import UUID

@dataclass
class Equino:
    animal_id: UUID
    aptidao: str | None = None