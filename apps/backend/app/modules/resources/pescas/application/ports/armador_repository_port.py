from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.resources.pescas.domain.models.armador import Armador

class ArmadorRepositoryPort(ABC):

    @abstractmethod
    async def save(self, armador: Armador) -> Armador:
        pass

    @abstractmethod
    async def get_by_id(self, armador_id: UUID) -> Armador | None:
        pass

    @abstractmethod
    async def get_by_nif(self, nif: str) -> Armador | None:
        pass

    @abstractmethod
    async def list_all(self, ativo: bool | None=None) -> list[Armador]:
        pass