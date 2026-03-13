from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.economy.trade.services.domain.enums import RamoComercial, StatusComercial
from apps.backend.app.modules.economy.trade.services.domain.models import EstabelecimentoComercial

class EstabelecimentoComercialRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: EstabelecimentoComercial) -> EstabelecimentoComercial:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> EstabelecimentoComercial | None:
        pass

    @abstractmethod
    async def get_by_cnpj(self, cnpj: str) -> EstabelecimentoComercial | None:
        pass

    @abstractmethod
    async def list(self, *, status: StatusComercial | None=None, ramo: RamoComercial | None=None, municipio: str | None=None) -> list[EstabelecimentoComercial]:
        pass