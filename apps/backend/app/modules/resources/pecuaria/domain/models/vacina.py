from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4


@dataclass
class Vacina:
    id: UUID
    animal_id: UUID
    nome: str
    data_aplicacao: date
    proxima_dose: date | None = None

    @classmethod
    def aplicar(
        cls, *, animal_id: UUID, nome: str, data_aplicacao: date, proxima_dose: date | None = None
    ) -> "Vacina":
        return cls(
            id=uuid4(),
            animal_id=animal_id,
            nome=nome,
            data_aplicacao=data_aplicacao,
            proxima_dose=proxima_dose,
        )
