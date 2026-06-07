from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.resources.agricultura.domain.enums import StatusProdutor
from apps.backend.app.modules.resources.agricultura.domain.models.produtor import Produtor


class ProdutorRepositoryPort(ABC):
    @abstractmethod
    async def save(self, produtor: Produtor) -> Produtor:
        pass

    @abstractmethod
    async def get_by_id(self, produtor_id: UUID) -> Produtor | None:
        pass

    @abstractmethod
    async def get_by_cadastro(self, cadastro_produtor: str) -> Produtor | None:
        pass

    @abstractmethod
    async def get_by_documento(self, documento: str) -> Produtor | None:
        pass

    @abstractmethod
    async def list_by_status(self, status: StatusProdutor | None = None) -> list[Produtor]:
        pass

    @abstractmethod
    async def next_cadastro(self) -> str:
        pass
