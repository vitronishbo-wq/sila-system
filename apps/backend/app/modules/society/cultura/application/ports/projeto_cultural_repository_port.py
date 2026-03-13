from __future__ import annotations
from datetime import date
from uuid import UUID
from app.modules.society.cultura.domain.enums import StatusProjetoCultural, TipoProjetoCultural
from app.modules.society.cultura.domain.models.projeto_cultural import ProjetoCultural

class ProjetoCulturalRepositoryPort:

    async def save(self, projeto: ProjetoCultural) -> ProjetoCultural:
        raise NotImplementedError

    async def get_by_id(self, projeto_id: UUID) -> ProjetoCultural | None:
        raise NotImplementedError

    async def get_by_codigo(self, codigo_projeto: str) -> ProjetoCultural | None:
        raise NotImplementedError

    async def list_all(self) -> list[ProjetoCultural]:
        raise NotImplementedError

    async def list_by_tipo(self, tipo: TipoProjetoCultural) -> list[ProjetoCultural]:
        raise NotImplementedError

    async def list_by_status(self, status: StatusProjetoCultural) -> list[ProjetoCultural]:
        raise NotImplementedError

    async def list_by_periodo(self, data_inicio: date, data_fim: date) -> list[ProjetoCultural]:
        raise NotImplementedError

    async def delete(self, projeto_id: UUID) -> bool:
        raise NotImplementedError

    async def next_codigo(self) -> str:
        raise NotImplementedError