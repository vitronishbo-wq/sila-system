from __future__ import annotations
from apps.backend.app.modules.governance.statistics.application.ports.dashboard_repository_port import DashboardRepositoryPort
from apps.backend.app.modules.governance.statistics.domain.models.dashboard import Dashboard
from apps.backend.app.modules.governance.statistics.exceptions import EstatisticaNotFoundError

class DashboardService:

    def __init__(self, dashboard_repository: DashboardRepositoryPort) -> None:
        self.dashboard_repository = dashboard_repository

    async def criar_dashboard(self, data: dict) -> Dashboard:
        dashboard = Dashboard(**data)
        return await self.dashboard_repository.create(dashboard)

    async def listar_dashboards(self, limit: int=100, offset: int=0) -> list[Dashboard]:
        return await self.dashboard_repository.list_all(limit=limit, offset=offset)

    async def obter_dashboard(self, dashboard_id: int) -> Dashboard:
        dashboard = await self.dashboard_repository.get_by_id(dashboard_id)
        if not dashboard:
            raise EstatisticaNotFoundError('Dashboard nao encontrado')
        return dashboard

    async def atualizar_dashboard(self, dashboard_id: int, data: dict) -> Dashboard:
        dashboard = await self.obter_dashboard(dashboard_id)
        for key, value in data.items():
            if value is not None and hasattr(dashboard, key):
                setattr(dashboard, key, value)
        return await self.dashboard_repository.update(dashboard)

    async def deletar_dashboard(self, dashboard_id: int) -> None:
        deleted = await self.dashboard_repository.delete(dashboard_id)
        if not deleted:
            raise EstatisticaNotFoundError('Dashboard nao encontrado')