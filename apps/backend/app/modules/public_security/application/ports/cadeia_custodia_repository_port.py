from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.public_security.domain.enums import StatusCadeiaCustodia
from app.modules.public_security.domain.models.cadeia_custodia import CadeiaCustodia

class CadeiaCustodiaRepositoryPort(ABC):

    @abstractmethod
    async def save(self, cadeia: CadeiaCustodia) -> CadeiaCustodia:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, cadeia_id: UUID) -> CadeiaCustodia | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_cadeia: str) -> CadeiaCustodia | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_prova(self, prova_id: UUID) -> CadeiaCustodia | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[CadeiaCustodia]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusCadeiaCustodia) -> list[CadeiaCustodia]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, cadeia_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError