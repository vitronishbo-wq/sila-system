from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.resources.florestas.domain.models.inventario_florestal import InventarioFlorestal

class InventarioFlorestalRepositoryPort(ABC):

    @abstractmethod
    async def save(self, inventario: InventarioFlorestal) -> InventarioFlorestal:
        pass

    @abstractmethod
    async def get_by_id(self, inventario_id: UUID) -> InventarioFlorestal | None:
        pass

    @abstractmethod
    async def list_by_unidade(self, unidade_manejo_id: UUID) -> list[InventarioFlorestal]:
        pass