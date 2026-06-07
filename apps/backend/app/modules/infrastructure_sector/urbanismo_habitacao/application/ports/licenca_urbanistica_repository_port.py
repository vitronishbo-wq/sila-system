from __future__ import annotations

from abc import ABC, abstractmethod

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import (
    StatusLicencaUrbanistica,
    TipoAlvara,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.licenca_urbanistica import (
    LicencaUrbanistica,
)


class LicencaUrbanisticaRepositoryPort(ABC):
    @abstractmethod
    async def save(self, item: LicencaUrbanistica) -> LicencaUrbanistica:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_licenca: str) -> LicencaUrbanistica | None:
        pass

    @abstractmethod
    async def list(
        self,
        *,
        status: StatusLicencaUrbanistica | None = None,
        tipo_alvara: TipoAlvara | None = None,
        provincia: str | None = None,
    ) -> list[LicencaUrbanistica]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass
