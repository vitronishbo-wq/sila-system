from __future__ import annotations
from abc import ABC, abstractmethod
from apps.backend.app.modules.governance.statistics.domain.enums import StatusKPI
from apps.backend.app.modules.governance.statistics.domain.models.kpi import KPI

class KPIRepositoryPort(ABC):

    @abstractmethod
    async def create(self, kpi: KPI) -> KPI:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, kpi_id: int) -> KPI | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_nome(self, nome: str) -> KPI | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self, limit: int=100, offset: int=0) -> list[KPI]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusKPI, limit: int=100) -> list[KPI]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, kpi: KPI) -> KPI:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, kpi_id: int) -> bool:
        raise NotImplementedError