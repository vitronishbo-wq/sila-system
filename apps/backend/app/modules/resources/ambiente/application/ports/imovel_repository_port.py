from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.resources.ambiente.domain.models.imovel_rural import ImovelRural

class ImovelRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: ImovelRural) -> ImovelRural:
        pass

    @abstractmethod
    async def get_by_id(self, imovel_id: UUID) -> ImovelRural | None:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_imovel: str) -> ImovelRural | None:
        pass

    @abstractmethod
    async def list_by_proprietario(self, proprietario_id: UUID) -> list[ImovelRural]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass