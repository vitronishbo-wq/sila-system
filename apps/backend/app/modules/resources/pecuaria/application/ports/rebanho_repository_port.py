from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.resources.pecuaria.domain.models.rebanho import Rebanho

class RebanhoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: Rebanho) -> Rebanho:
        pass

    @abstractmethod
    async def get_by_id(self, rebanho_id: UUID) -> Rebanho | None:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_rebanho: str) -> Rebanho | None:
        pass

    @abstractmethod
    async def list_by_propriedade(self, propriedade_id: UUID | None=None) -> list[Rebanho]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass