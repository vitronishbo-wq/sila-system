from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.infrastructure.domain.enums import StatusEdital
from apps.backend.app.modules.infrastructure.domain.models.edital import Edital

class EditalRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: Edital) -> Edital:
        pass

    @abstractmethod
    async def get_by_numero(self, numero_edital: str) -> Edital | None:
        pass

    @abstractmethod
    async def list(self, *, status: StatusEdital | None=None, licitacao_id: UUID | None=None) -> list[Edital]:
        pass

    @abstractmethod
    async def next_numero(self) -> str:
        pass