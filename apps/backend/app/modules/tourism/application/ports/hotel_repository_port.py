from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.tourism.domain.enums import ClassificacaoHoteleira
from apps.backend.app.modules.tourism.domain.models.hotel import Hotel

class HotelRepositoryPort(ABC):

    @abstractmethod
    async def save(self, hotel: Hotel) -> Hotel:
        pass

    @abstractmethod
    async def get_by_id(self, hotel_id: UUID) -> Hotel | None:
        pass

    @abstractmethod
    async def get_by_cadastur(self, cadastur: str) -> Hotel | None:
        pass

    @abstractmethod
    async def get_by_cnpj(self, cnpj: str) -> Hotel | None:
        pass

    @abstractmethod
    async def list_all(self) -> list[Hotel]:
        pass

    @abstractmethod
    async def list_by_proprietario(self, proprietario_id: UUID) -> list[Hotel]:
        pass

    @abstractmethod
    async def list_by_municipio(self, municipio: str) -> list[Hotel]:
        pass

    @abstractmethod
    async def list_by_classificacao(self, classificacao: ClassificacaoHoteleira) -> list[Hotel]:
        pass

    @abstractmethod
    async def next_cadastur(self, provincia: str) -> str:
        pass