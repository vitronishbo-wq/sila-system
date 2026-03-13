from __future__ import annotations
from abc import ABC, abstractmethod
from app.modules.resources.ambiente.domain.enums import StatusEmbargo
from app.modules.resources.ambiente.domain.models.embargo import Embargo

class EmbargoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: Embargo) -> Embargo:
        pass

    @abstractmethod
    async def get_by_numero(self, numero_embargo: str) -> Embargo | None:
        pass

    @abstractmethod
    async def list(self, *, numero_auto_infracao: str | None=None, status: StatusEmbargo | None=None) -> list[Embargo]:
        pass

    @abstractmethod
    async def next_numero(self) -> str:
        pass