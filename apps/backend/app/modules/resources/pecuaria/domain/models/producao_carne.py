from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

@dataclass
class ProducaoCarne:
    id: UUID
    propriedade_id: UUID
    quilos: float
    data_producao: date

    @classmethod
    def registrar(cls, *, propriedade_id: UUID, quilos: float, data_producao: date) -> 'ProducaoCarne':
        if quilos <= 0:
            raise ValueError('Quilos devem ser maiores que zero')
        return cls(id=uuid4(), propriedade_id=propriedade_id, quilos=round(quilos, 2), data_producao=data_producao)