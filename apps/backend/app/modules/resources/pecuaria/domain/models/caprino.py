from dataclasses import dataclass
from uuid import UUID


@dataclass
class Caprino:
    animal_id: UUID
    aptidao: str | None = None
