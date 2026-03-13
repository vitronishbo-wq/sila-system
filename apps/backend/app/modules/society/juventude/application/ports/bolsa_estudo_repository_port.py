from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.society.juventude.domain.models.bolsa_estudo import BolsaEstudo

class BolsaEstudoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, bolsa: BolsaEstudo) -> BolsaEstudo:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, bolsa_id: UUID) -> BolsaEstudo | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_bolsa: str) -> BolsaEstudo | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[BolsaEstudo]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_jovem(self, jovem_id: UUID) -> list[BolsaEstudo]:
        raise NotImplementedError

    @abstractmethod
    async def list_ativas(self) -> list[BolsaEstudo]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, bolsa_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError