from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.civil_protection.domain.enums import StatusCorporacao
from app.modules.civil_protection.domain.models.corporacao import Corporacao

class CorporacaoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, corporacao: Corporacao) -> Corporacao:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, corporacao_id: UUID) -> Corporacao | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_corporacao: str) -> Corporacao | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Corporacao]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_municipio(self, municipio: str) -> list[Corporacao]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusCorporacao) -> list[Corporacao]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, corporacao_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError