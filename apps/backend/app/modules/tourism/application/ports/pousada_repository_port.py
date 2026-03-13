from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.tourism.domain.enums import ClassificacaoHoteleira
from apps.backend.app.modules.tourism.domain.models.pousada import Pousada

class PousadaRepositoryPort(ABC):

    @abstractmethod
    async def save(self, pousada: Pousada) -> Pousada:
        pass

    @abstractmethod
    async def get_by_id(self, pousada_id: UUID) -> Pousada | None:
        pass

    @abstractmethod
    async def get_by_cnpj(self, cnpj: str) -> Pousada | None:
        pass

    @abstractmethod
    async def get_by_cadastur(self, cadastur: str) -> Pousada | None:
        pass

    @abstractmethod
    async def list(self, *, municipio: str | None=None, classificacao: ClassificacaoHoteleira | None=None, ativa: bool | None=None) -> list[Pousada]:
        pass

    @abstractmethod
    async def delete(self, pousada_id: UUID) -> bool:
        pass

    @abstractmethod
    async def next_cadastur(self, provincia: str) -> str:
        pass
