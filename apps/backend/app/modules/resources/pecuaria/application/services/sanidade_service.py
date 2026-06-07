from __future__ import annotations

from datetime import date
from uuid import UUID

from apps.backend.app.modules.resources.pecuaria.domain.models.vacina import Vacina


class SanidadeService:
    def __init__(self) -> None:
        self._vacinas: dict[UUID, Vacina] = {}

    async def aplicar_vacina(
        self, *, animal_id: UUID, nome: str, data_aplicacao: date, proxima_dose: date | None = None
    ) -> Vacina:
        item = Vacina.aplicar(
            animal_id=animal_id, nome=nome, data_aplicacao=data_aplicacao, proxima_dose=proxima_dose
        )
        self._vacinas[item.id] = item
        return item

    async def listar_vacinas(self, animal_id: UUID | None = None) -> list[Vacina]:
        values = list(self._vacinas.values())
        if animal_id:
            values = [item for item in values if item.animal_id == animal_id]
        return values
