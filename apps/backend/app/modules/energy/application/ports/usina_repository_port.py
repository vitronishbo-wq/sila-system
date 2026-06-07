from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.energy.domain.enums import FonteEnergia, StatusUsina
from apps.backend.app.modules.energy.domain.models import Usina


class UsinaRepositoryPort(ABC):
    @abstractmethod
    async def save(self, usina: Usina) -> Usina:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Usina | None:
        pass

    @abstractmethod
    async def get_by_codigo_aneel(self, codigo_aneel: str) -> Usina | None:
        pass

    @abstractmethod
    async def list(
        self,
        *,
        status: StatusUsina | None = None,
        fonte: FonteEnergia | None = None,
        provincia: str | None = None,
    ) -> list[Usina]:
        pass
