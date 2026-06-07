from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.energy.domain.enums import StatusInfraEnergia
from apps.backend.app.modules.energy.domain.models import LinhaTransmissao


class LinhaTransmissaoRepositoryPort(ABC):
    @abstractmethod
    async def save(self, item: LinhaTransmissao) -> LinhaTransmissao:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> LinhaTransmissao | None:
        pass

    @abstractmethod
    async def list(self, *, status: StatusInfraEnergia | None = None) -> list[LinhaTransmissao]:
        pass

    @abstractmethod
    async def list_all(self) -> list[LinhaTransmissao]:
        pass
