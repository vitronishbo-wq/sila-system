from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4


@dataclass
class Inseminacao:
    id: UUID
    femea_id: UUID
    data_inseminacao: date
    semen_raca: str | None = None

    @classmethod
    def registrar(
        cls, *, femea_id: UUID, data_inseminacao: date, semen_raca: str | None = None
    ) -> "Inseminacao":
        return cls(
            id=uuid4(), femea_id=femea_id, data_inseminacao=data_inseminacao, semen_raca=semen_raca
        )
