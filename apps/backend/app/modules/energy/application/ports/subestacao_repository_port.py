from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.energy.domain.enums import StatusInfraEnergia
from apps.backend.app.modules.energy.domain.models import Subestacao

class SubestacaoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: Subestacao) -> Subestacao:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Subestacao | None:
        pass

    @abstractmethod
    async def list(self, *, status: StatusInfraEnergia | None=None) -> list[Subestacao]:
        pass

    @abstractmethod
    async def list_all(self) -> list[Subestacao]:
        pass
