from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.public_security.domain.enums import StatusUnidadePolicial
from app.modules.public_security.domain.models.unidade_policial import UnidadePolicial

class UnidadePolicialRepositoryPort(ABC):

    @abstractmethod
    async def save(self, unidade: UnidadePolicial) -> UnidadePolicial:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, unidade_id: UUID) -> UnidadePolicial | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_unidade: str) -> UnidadePolicial | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[UnidadePolicial]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_municipio(self, municipio: str) -> list[UnidadePolicial]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusUnidadePolicial) -> list[UnidadePolicial]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, unidade_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError