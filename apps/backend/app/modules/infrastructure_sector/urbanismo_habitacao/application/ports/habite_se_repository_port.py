from __future__ import annotations
from abc import ABC, abstractmethod
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusHabiteSe, TipoHabiteSe
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.habite_se import HabiteSe

class HabiteSeRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: HabiteSe) -> HabiteSe:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_habite_se: str) -> HabiteSe | None:
        pass

    @abstractmethod
    async def list(self, *, status: StatusHabiteSe | None=None, tipo: TipoHabiteSe | None=None, provincia: str | None=None) -> list[HabiteSe]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass