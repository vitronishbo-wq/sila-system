from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.society.cultura.domain.enums import StatusTombamento, TipoPatrimonio
from app.modules.society.cultura.domain.models.bem_cultural import BemCultural

class BemCulturalRepositoryPort(ABC):

    @abstractmethod
    async def save(self, bem: BemCultural) -> BemCultural:
        pass

    @abstractmethod
    async def get_by_id(self, bem_id: UUID) -> BemCultural | None:
        pass

    @abstractmethod
    async def get_by_registro(self, registro_ipat: str) -> BemCultural | None:
        pass

    @abstractmethod
    async def list_all(self) -> list[BemCultural]:
        pass

    @abstractmethod
    async def list_by_tipo(self, tipo: TipoPatrimonio) -> list[BemCultural]:
        pass

    @abstractmethod
    async def list_by_municipio(self, municipio: str) -> list[BemCultural]:
        pass

    @abstractmethod
    async def list_by_status_tombamento(self, status: StatusTombamento) -> list[BemCultural]:
        pass

    @abstractmethod
    async def delete(self, bem_id: UUID) -> bool:
        pass

    @abstractmethod
    async def next_registro(self) -> str:
        pass