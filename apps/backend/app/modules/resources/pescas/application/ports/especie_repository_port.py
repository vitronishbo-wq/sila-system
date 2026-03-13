from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.resources.pescas.domain.models.especie import Especie

class EspecieRepositoryPort(ABC):

    @abstractmethod
    async def save(self, especie: Especie) -> Especie:
        pass

    @abstractmethod
    async def get_by_id(self, especie_id: UUID) -> Especie | None:
        pass

    @abstractmethod
    async def get_by_codigo_fao(self, codigo_fao: str) -> Especie | None:
        pass

    @abstractmethod
    async def list_all(self) -> list[Especie]:
        pass