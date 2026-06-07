from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4


@dataclass
class Comercializacao:
    id: UUID
    propriedade_id: UUID
    descricao: str
    valor_total: float
    data_evento: date

    @classmethod
    def registrar(
        cls, *, propriedade_id: UUID, descricao: str, valor_total: float, data_evento: date
    ) -> "Comercializacao":
        if valor_total <= 0:
            raise ValueError("Valor deve ser maior que zero")
        return cls(
            id=uuid4(),
            propriedade_id=propriedade_id,
            descricao=descricao,
            valor_total=round(valor_total, 2),
            data_evento=data_evento,
        )
