from __future__ import annotations
from datetime import UTC, datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.governance.statistics.application.ports.dashboard_repository_port import DashboardRepositoryPort
from apps.backend.app.modules.governance.statistics.domain.enums import TipoDashboard
from apps.backend.app.modules.governance.statistics.domain.models.dashboard import Dashboard
from apps.backend.app.modules.governance.statistics.infrastructure.models.dashboard_model import DashboardModel

class SQLAlchemyDashboardRepository(DashboardRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, dashboard: Dashboard) -> Dashboard:
        model = DashboardModel(nome=dashboard.nome, descricao=dashboard.descricao, tipo=dashboard.tipo.value, configuracoes=dashboard.configuracoes, kpi_ids=dashboard.kpi_ids, criado_por=dashboard.criado_por)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, dashboard_id: int) -> Dashboard | None:
        model = await self.session.get(DashboardModel, dashboard_id)
        return self._to_domain(model) if model else None

    async def list_all(self, limit: int=100, offset: int=0) -> list[Dashboard]:
        stmt = select(DashboardModel).order_by(DashboardModel.nome.asc()).offset(offset).limit(limit)
        models = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(m) for m in models]

    async def update(self, dashboard: Dashboard) -> Dashboard:
        model = await self.session.get(DashboardModel, dashboard.id)
        if model is None:
            raise ValueError('Dashboard nao encontrado')
        model.nome = dashboard.nome
        model.descricao = dashboard.descricao
        model.tipo = dashboard.tipo.value
        model.configuracoes = dashboard.configuracoes
        model.kpi_ids = dashboard.kpi_ids
        model.criado_por = dashboard.criado_por
        model.data_atualizacao = datetime.now(UTC)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def delete(self, dashboard_id: int) -> bool:
        model = await self.session.get(DashboardModel, dashboard_id)
        if model is None:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    @staticmethod
    def _to_domain(model: DashboardModel) -> Dashboard:
        return Dashboard(id=model.id, nome=model.nome, descricao=model.descricao, tipo=TipoDashboard(model.tipo), configuracoes=model.configuracoes, kpi_ids=model.kpi_ids or [], criado_por=model.criado_por, data_criacao=model.data_criacao, data_atualizacao=model.data_atualizacao or model.data_criacao)