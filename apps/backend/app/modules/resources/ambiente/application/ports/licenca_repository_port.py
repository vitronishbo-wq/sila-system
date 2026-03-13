from __future__ import annotations
from abc import ABC, abstractmethod
from apps.backend.app.modules.resources.ambiente.domain.enums import StatusLicenca, TipoLicenca
from apps.backend.app.modules.resources.ambiente.domain.models.licenca_ambiental import LicencaAmbiental

class LicencaRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: LicencaAmbiental) -> LicencaAmbiental:
        pass

    @abstractmethod
    async def get_by_numero(self, numero_licenca: str) -> LicencaAmbiental | None:
        pass

    @abstractmethod
    async def list(self, *, numero_car: str | None=None, tipo: TipoLicenca | None=None, status: StatusLicenca | None=None) -> list[LicencaAmbiental]:
        pass

    @abstractmethod
    async def next_numero(self) -> str:
        pass