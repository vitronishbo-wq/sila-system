from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.resources.pescas.domain.models.rastreabilidade_pesca import RastreabilidadePesca

class RastreabilidadePescaRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: RastreabilidadePesca) -> RastreabilidadePesca:
        pass

    @abstractmethod
    async def get_by_id(self, item_id: UUID) -> RastreabilidadePesca | None:
        pass

    @abstractmethod
    async def list_by_lote(self, lote_codigo: str) -> list[RastreabilidadePesca]:
        pass

    @abstractmethod
    async def list_by_captura(self, captura_id: UUID) -> list[RastreabilidadePesca]:
        pass