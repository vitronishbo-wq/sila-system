from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.society.desporto.domain.models.estadio import Estadio

class EstadioRepositoryPort(ABC):

    @abstractmethod
    async def save(self, estadio: Estadio) -> Estadio:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, estadio_id: UUID) -> Estadio | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_estadio: str) -> Estadio | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Estadio]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_municipio(self, municipio: str) -> list[Estadio]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, estadio_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError