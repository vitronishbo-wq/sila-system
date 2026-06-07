from dataclasses import dataclass
from uuid import UUID


@dataclass
class Ovino:
    animal_id: UUID
    aptidao: str | None = None
