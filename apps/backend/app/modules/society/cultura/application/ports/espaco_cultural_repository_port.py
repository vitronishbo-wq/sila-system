from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.society.cultura.domain.enums import TipoEspacoCultural
from apps.backend.app.modules.society.cultura.domain.models.espaco_cultural import EspacoCultural


class EspacoCulturalRepositoryPort:
    async def save(self, espaco: EspacoCultural) -> EspacoCultural:
        raise NotImplementedError

    async def get_by_id(self, espaco_id: UUID) -> EspacoCultural | None:
        raise NotImplementedError

    async def get_by_codigo(self, codigo_espaco: str) -> EspacoCultural | None:
        raise NotImplementedError

    async def list_all(self) -> list[EspacoCultural]:
        raise NotImplementedError

    async def list_by_tipo(self, tipo: TipoEspacoCultural) -> list[EspacoCultural]:
        raise NotImplementedError

    async def list_by_municipio(self, municipio: str) -> list[EspacoCultural]:
        raise NotImplementedError

    async def delete(self, espaco_id: UUID) -> bool:
        raise NotImplementedError

    async def next_codigo(self) -> str:
        raise NotImplementedError
