from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.logistics.domain.enums import StatusFrota
from apps.backend.app.modules.logistics.domain.models import Frota


class FrotaRepositoryPort(ABC):
    @abstractmethod
    async def save(self, item: Frota) -> Frota:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_frota: str) -> Frota | None:
        pass

    @abstractmethod
    async def list(
        self,
        *,
        status: StatusFrota | None = None,
        operadora_id: UUID | None = None,
        municipio: str | None = None,
        provincia: str | None = None,
    ) -> list[Frota]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass
