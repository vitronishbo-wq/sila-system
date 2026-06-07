from __future__ import annotations

from abc import ABC, abstractmethod

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import (
    StatusAlvara,
    TipoAlvara,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.alvara import (
    Alvara,
)


class AlvaraRepositoryPort(ABC):
    @abstractmethod
    async def save(self, item: Alvara) -> Alvara:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_alvara: str) -> Alvara | None:
        pass

    @abstractmethod
    async def list(
        self,
        *,
        status: StatusAlvara | None = None,
        tipo: TipoAlvara | None = None,
        provincia: str | None = None,
    ) -> list[Alvara]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass
