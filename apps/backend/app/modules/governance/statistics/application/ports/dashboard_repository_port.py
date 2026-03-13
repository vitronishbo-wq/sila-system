from __future__ import annotations
from abc import ABC, abstractmethod
from apps.backend.app.modules.governance.statistics.domain.models.dashboard import Dashboard

class DashboardRepositoryPort(ABC):

    @abstractmethod
    async def create(self, dashboard: Dashboard) -> Dashboard:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, dashboard_id: int) -> Dashboard | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self, limit: int=100, offset: int=0) -> list[Dashboard]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, dashboard: Dashboard) -> Dashboard:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, dashboard_id: int) -> bool:
        raise NotImplementedError