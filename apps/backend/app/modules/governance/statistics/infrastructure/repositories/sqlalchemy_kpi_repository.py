from __future__ import annotations
from datetime import UTC, datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.governance.statistics.application.ports.kpi_repository_port import KPIRepositoryPort
from app.modules.governance.statistics.domain.enums import StatusKPI
from app.modules.governance.statistics.domain.models.kpi import KPI
from app.modules.governance.statistics.infrastructure.models.kpi_model import KPIModel

class SQLAlchemyKPIRepository(KPIRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, kpi: KPI) -> KPI:
        model = KPIModel(nome=kpi.nome, descricao=kpi.descricao, metrica_id=kpi.metrica_id, valor_alvo=kpi.valor_alvo, valor_atual=kpi.valor_atual, valor_anterior=kpi.valor_anterior, unidade=kpi.unidade, status=kpi.status.value, peso=kpi.peso, limite_inferior=kpi.limite_inferior, limite_superior=kpi.limite_superior)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, kpi_id: int) -> KPI | None:
        model = await self.session.get(KPIModel, kpi_id)
        return self._to_domain(model) if model else None

    async def get_by_nome(self, nome: str) -> KPI | None:
        stmt = select(KPIModel).where(KPIModel.nome == nome)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self, limit: int=100, offset: int=0) -> list[KPI]:
        stmt = select(KPIModel).order_by(KPIModel.nome.asc()).offset(offset).limit(limit)
        models = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(m) for m in models]

    async def list_by_status(self, status: StatusKPI, limit: int=100) -> list[KPI]:
        stmt = select(KPIModel).where(KPIModel.status == status.value).order_by(KPIModel.nome.asc()).limit(limit)
        models = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(m) for m in models]

    async def update(self, kpi: KPI) -> KPI:
        model = await self.session.get(KPIModel, kpi.id)
        if model is None:
            raise ValueError('KPI nao encontrado')
        model.nome = kpi.nome
        model.descricao = kpi.descricao
        model.metrica_id = kpi.metrica_id
        model.valor_alvo = kpi.valor_alvo
        model.valor_atual = kpi.valor_atual
        model.valor_anterior = kpi.valor_anterior
        model.unidade = kpi.unidade
        model.status = kpi.status.value
        model.peso = kpi.peso
        model.limite_inferior = kpi.limite_inferior
        model.limite_superior = kpi.limite_superior
        model.data_atualizacao = datetime.now(UTC)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def delete(self, kpi_id: int) -> bool:
        model = await self.session.get(KPIModel, kpi_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    @staticmethod
    def _to_domain(model: KPIModel) -> KPI:
        return KPI(id=model.id, nome=model.nome, descricao=model.descricao, metrica_id=model.metrica_id, valor_alvo=model.valor_alvo, valor_atual=model.valor_atual, valor_anterior=model.valor_anterior, unidade=model.unidade, status=StatusKPI(model.status), peso=model.peso, limite_inferior=model.limite_inferior, limite_superior=model.limite_superior, data_criacao=model.data_criacao, data_atualizacao=model.data_atualizacao or model.data_criacao)