from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4


@dataclass
class Alimentacao:
    id: UUID
    animal_id: UUID
    descricao: str
    data_registro: date

    @classmethod
    def registrar(cls, *, animal_id: UUID, descricao: str) -> "Alimentacao":
        return cls(id=uuid4(), animal_id=animal_id, descricao=descricao, data_registro=date.today())
