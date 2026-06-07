from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.industry.domain.enums import RamoIndustrial, StatusEstabelecimento
from apps.backend.app.modules.industry.domain.models import EstabelecimentoIndustrial


class EstabelecimentoIndustrialRepositoryPort(ABC):
    @abstractmethod
    async def save(self, item: EstabelecimentoIndustrial) -> EstabelecimentoIndustrial:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> EstabelecimentoIndustrial | None:
        pass

    @abstractmethod
    async def get_by_cnpj(self, cnpj: str) -> EstabelecimentoIndustrial | None:
        pass

    @abstractmethod
    async def list(
        self,
        *,
        status: StatusEstabelecimento | None = None,
        ramo: RamoIndustrial | None = None,
        municipio: str | None = None,
    ) -> list[EstabelecimentoIndustrial]:
        pass
