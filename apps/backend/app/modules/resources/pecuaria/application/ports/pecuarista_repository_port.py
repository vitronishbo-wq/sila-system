from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.resources.pecuaria.domain.enums import StatusPecuarista
from app.modules.resources.pecuaria.domain.models.pecuarista import Pecuarista

class PecuaristaRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: Pecuarista) -> Pecuarista:
        pass

    @abstractmethod
    async def get_by_id(self, pecuarista_id: UUID) -> Pecuarista | None:
        pass

    @abstractmethod
    async def get_by_cadastro(self, cadastro_pecuarista: str) -> Pecuarista | None:
        pass

    @abstractmethod
    async def get_by_documento(self, documento: str) -> Pecuarista | None:
        pass

    @abstractmethod
    async def list_by_status(self, status: StatusPecuarista | None=None) -> list[Pecuarista]:
        pass

    @abstractmethod
    async def next_cadastro(self) -> str:
        pass