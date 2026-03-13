from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.governance.cooperacao_internacional.domain.models.visto import Visto

class VistoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, visto: Visto) -> Visto:
        ...

    @abstractmethod
    async def get_by_id(self, visto_id: UUID) -> Visto | None:
        ...

    @abstractmethod
    async def list_all(self) -> list[Visto]:
        ...