from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.resources.pescas.domain.models.defeso import Defeso

class DefesoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, defeso: Defeso) -> Defeso:
        pass

    @abstractmethod
    async def get_by_id(self, defeso_id: UUID) -> Defeso | None:
        pass

    @abstractmethod
    async def list_ativos(self) -> list[Defeso]:
        pass

    @abstractmethod
    async def list_by_especie(self, especie_id: UUID) -> list[Defeso]:
        pass