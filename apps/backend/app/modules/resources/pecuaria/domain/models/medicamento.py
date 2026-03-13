from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

@dataclass
class Medicamento:
    id: UUID
    animal_id: UUID
    nome: str
    dosagem: str
    data_registro: date

    @classmethod
    def registrar(cls, *, animal_id: UUID, nome: str, dosagem: str) -> 'Medicamento':
        return cls(id=uuid4(), animal_id=animal_id, nome=nome, dosagem=dosagem, data_registro=date.today())