from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class Pasto:
    id: UUID
    propriedade_id: UUID
    nome: str
    area_ha: float

    @classmethod
    def criar(cls, *, propriedade_id: UUID, nome: str, area_ha: float) -> "Pasto":
        return cls(id=uuid4(), propriedade_id=propriedade_id, nome=nome, area_ha=round(area_ha, 2))
