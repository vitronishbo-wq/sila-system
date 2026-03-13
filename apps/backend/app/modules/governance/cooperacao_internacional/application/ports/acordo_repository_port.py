from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.governance.cooperacao_internacional.domain.models.acordo import Acordo

class AcordoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, acordo: Acordo) -> Acordo:
        ...

    @abstractmethod
    async def get_by_id(self, acordo_id: UUID) -> Acordo | None:
        ...

    @abstractmethod
    async def list_all(self) -> list[Acordo]:
        ...

    @abstractmethod
    async def find_em_vigor(self) -> list[Acordo]:
        ...