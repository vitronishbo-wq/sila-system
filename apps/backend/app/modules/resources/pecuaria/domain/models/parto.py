from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

@dataclass
class Parto:
    id: UUID
    matriz_id: UUID
    data_parto: date
    crias_vivas: int

    @classmethod
    def registrar(cls, *, matriz_id: UUID, data_parto: date, crias_vivas: int) -> 'Parto':
        if crias_vivas < 0:
            raise ValueError('Quantidade de crias vivas nao pode ser negativa')
        return cls(id=uuid4(), matriz_id=matriz_id, data_parto=data_parto, crias_vivas=crias_vivas)