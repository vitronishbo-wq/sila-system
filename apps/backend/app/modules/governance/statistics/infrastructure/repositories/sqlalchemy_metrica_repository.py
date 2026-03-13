from __future__ import annotations
from datetime import UTC, datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.governance.statistics.application.ports.metrica_repository_port import MetricaRepositoryPort
from apps.backend.app.modules.governance.statistics.domain.enums import FonteDados, Periodicidade, TipoMetrica
from apps.backend.app.modules.governance.statistics.domain.models.metrica import Metrica
from apps.backend.app.modules.governance.statistics.infrastructure.models.metrica_model import MetricaModel

class SQLAlchemyMetricaRepository(MetricaRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, metrica: Metrica) -> Metrica:
        model = MetricaModel(nome=metrica.nome, descricao=metrica.descricao, tipo=metrica.tipo.value, unidade=metrica.unidade, fonte_dados=metrica.fonte_dados.value, periodicidade=metrica.periodicidade.value, formula=metrica.formula, parametros=metrica.parametros, valor_atual=metrica.valor_atual, valor_anterior=metrica.valor_anterior, variacao_percentual=metrica.variacao_percentual, ativo=metrica.ativo, ultima_atualizacao=metrica.ultima_atualizacao)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, metrica_id: int) -> Metrica | None:
        model = await self.session.get(MetricaModel, metrica_id)
        return self._to_domain(model) if model else None

    async def get_by_nome(self, nome: str) -> Metrica | None:
        stmt = select(MetricaModel).where(MetricaModel.nome == nome)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self, limit: int=100, offset: int=0) -> list[Metrica]:
        stmt = select(MetricaModel).order_by(MetricaModel.nome.asc()).offset(offset).limit(limit)
        models = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(m) for m in models]

    async def list_by_fonte(self, fonte: FonteDados, limit: int=100) -> list[Metrica]:
        stmt = select(MetricaModel).where(MetricaModel.fonte_dados == fonte.value).order_by(MetricaModel.nome.asc()).limit(limit)
        models = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(m) for m in models]

    async def list_by_tipo(self, tipo: TipoMetrica, limit: int=100) -> list[Metrica]:
        stmt = select(MetricaModel).where(MetricaModel.tipo == tipo.value).order_by(MetricaModel.nome.asc()).limit(limit)
        models = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(m) for m in models]

    async def update(self, metrica: Metrica) -> Metrica:
        model = await self.session.get(MetricaModel, metrica.id)
        if model is None:
            raise ValueError('Metrica nao encontrada')
        model.nome = metrica.nome
        model.descricao = metrica.descricao
        model.tipo = metrica.tipo.value
        model.unidade = metrica.unidade
        model.fonte_dados = metrica.fonte_dados.value
        model.periodicidade = metrica.periodicidade.value
        model.formula = metrica.formula
        model.parametros = metrica.parametros
        model.valor_atual = metrica.valor_atual
        model.valor_anterior = metrica.valor_anterior
        model.variacao_percentual = metrica.variacao_percentual
        model.ativo = metrica.ativo
        model.ultima_atualizacao = metrica.ultima_atualizacao
        model.data_atualizacao = datetime.now(UTC)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def delete(self, metrica_id: int) -> bool:
        model = await self.session.get(MetricaModel, metrica_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    @staticmethod
    def _to_domain(model: MetricaModel) -> Metrica:
        return Metrica(id=model.id, nome=model.nome, descricao=model.descricao, tipo=TipoMetrica(model.tipo), unidade=model.unidade, fonte_dados=FonteDados(model.fonte_dados), periodicidade=Periodicidade(model.periodicidade), formula=model.formula, parametros=model.parametros, valor_atual=model.valor_atual, valor_anterior=model.valor_anterior, variacao_percentual=model.variacao_percentual, ativo=model.ativo, data_criacao=model.data_criacao, data_atualizacao=model.data_atualizacao or model.data_criacao, ultima_atualizacao=model.ultima_atualizacao)