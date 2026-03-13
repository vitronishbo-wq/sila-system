from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.society.cultura.domain.enums import TipoArtista
from apps.backend.app.modules.society.cultura.domain.models.artista import Artista

class ArtistaRepositoryPort(ABC):

    @abstractmethod
    async def save(self, artista: Artista) -> Artista:
        pass

    @abstractmethod
    async def get_by_id(self, artista_id: UUID) -> Artista | None:
        pass

    @abstractmethod
    async def get_by_registro(self, registro_cultural: str) -> Artista | None:
        pass

    @abstractmethod
    async def list_all(self) -> list[Artista]:
        pass

    @abstractmethod
    async def list_by_tipo(self, tipo: TipoArtista) -> list[Artista]:
        pass

    @abstractmethod
    async def delete(self, artista_id: UUID) -> bool:
        pass

    @abstractmethod
    async def next_registro(self) -> str:
        pass