from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

@dataclass
class ProducaoLeite:
    id: UUID
    propriedade_id: UUID
    litros: float
    data_producao: date

    @classmethod
    def registrar(cls, *, propriedade_id: UUID, litros: float, data_producao: date) -> 'ProducaoLeite':
        if litros <= 0:
            raise ValueError('Litros devem ser maiores que zero')
        return cls(id=uuid4(), propriedade_id=propriedade_id, litros=round(litros, 2), data_producao=data_producao)