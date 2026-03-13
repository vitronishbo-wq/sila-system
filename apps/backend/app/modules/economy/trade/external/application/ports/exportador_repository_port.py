from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.economy.trade.external.domain.enums import StatusHabilitacao
from apps.backend.app.modules.economy.trade.external.domain.models import Exportador

class ExportadorRepositoryPort(ABC):

    @abstractmethod
    async def save(self, exportador: Exportador) -> Exportador:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Exportador | None:
        pass

    @abstractmethod
    async def get_by_cnpj_cpf(self, cnpj_cpf: str) -> Exportador | None:
        pass

    @abstractmethod
    async def list(self, *, status: StatusHabilitacao | None=None, municipio: str | None=None) -> list[Exportador]:
        pass