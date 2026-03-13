from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.energy.domain.enums import FonteEnergia, StatusInfraEnergia
from app.modules.energy.domain.models import CentralGeradora

class CentralGeradoraRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: CentralGeradora) -> CentralGeradora:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> CentralGeradora | None:
        pass

    @abstractmethod
    async def list(self, *, status: StatusInfraEnergia | None=None, tipo: FonteEnergia | None=None) -> list[CentralGeradora]:
        pass

    @abstractmethod
    async def list_all(self) -> list[CentralGeradora]:
        pass
