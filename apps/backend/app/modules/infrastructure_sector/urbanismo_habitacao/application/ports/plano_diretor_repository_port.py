from __future__ import annotations
from abc import ABC, abstractmethod
from app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusPlanoDiretor, TipoPlanoDiretor
from app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.plano_diretor import PlanoDiretor

class PlanoDiretorRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: PlanoDiretor) -> PlanoDiretor:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_plano: str) -> PlanoDiretor | None:
        pass

    @abstractmethod
    async def list(self, *, status: StatusPlanoDiretor | None=None, tipo: TipoPlanoDiretor | None=None, provincia: str | None=None) -> list[PlanoDiretor]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass