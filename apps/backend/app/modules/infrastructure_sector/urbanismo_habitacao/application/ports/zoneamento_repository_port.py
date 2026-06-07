from __future__ import annotations

from abc import ABC, abstractmethod

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import (
    StatusZoneamento,
    TipoZona,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.zoneamento import (
    Zoneamento,
)


class ZoneamentoRepositoryPort(ABC):
    @abstractmethod
    async def save(self, item: Zoneamento) -> Zoneamento:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_zoneamento: str) -> Zoneamento | None:
        pass

    @abstractmethod
    async def list(
        self,
        *,
        status: StatusZoneamento | None = None,
        tipo_zona: TipoZona | None = None,
        provincia: str | None = None,
    ) -> list[Zoneamento]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass
