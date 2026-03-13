from dataclasses import dataclass
from uuid import UUID

@dataclass
class Suino:
    animal_id: UUID
    aptidao: str | None = None