from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.society.cultura.domain.enums import TipoGrupoArtistico
from apps.backend.app.modules.society.cultura.domain.models.grupo_artistico import GrupoArtistico


class GrupoArtisticoRepositoryPort(ABC):
    @abstractmethod
    async def save(self, grupo: GrupoArtistico) -> GrupoArtistico:
        pass

    @abstractmethod
    async def get_by_id(self, grupo_id: UUID) -> GrupoArtistico | None:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_grupo: str) -> GrupoArtistico | None:
        pass

    @abstractmethod
    async def list_all(self) -> list[GrupoArtistico]:
        pass

    @abstractmethod
    async def list_by_tipo(self, tipo: TipoGrupoArtistico) -> list[GrupoArtistico]:
        pass

    @abstractmethod
    async def list_by_municipio(self, municipio: str) -> list[GrupoArtistico]:
        pass

    @abstractmethod
    async def delete(self, grupo_id: UUID) -> bool:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass
