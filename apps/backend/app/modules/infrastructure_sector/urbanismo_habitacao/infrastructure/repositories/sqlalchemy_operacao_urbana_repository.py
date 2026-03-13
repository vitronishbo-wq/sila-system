from __future__ import annotations
from datetime import date
from decimal import Decimal
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.operacao_urbana_repository_port import OperacaoUrbanaRepositoryPort
from app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusOperacaoUrbana, TipoOperacaoUrbana
from app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.operacao_urbana import OperacaoUrbana
from app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.operacao_urbana_model import OperacaoUrbanaModel

class SQLAlchemyOperacaoUrbanaRepository(OperacaoUrbanaRepositoryPort):
    """Repository com ORM real (AsyncSession) e fallback em memoria."""

    def __init__(self, session: AsyncSession | None=None) -> None:
        self._session = session
        self._items: dict[str, OperacaoUrbana] = {}
        self._seq = 0

    async def save(self, item: OperacaoUrbana) -> OperacaoUrbana:
        if self._session:
            existing = await self._session.execute(select(OperacaoUrbanaModel).where(OperacaoUrbanaModel.codigo_operacao == item.codigo_operacao))
            model = existing.scalars().first()
            if model is None:
                model = OperacaoUrbanaModel(id=item.id, codigo_operacao=item.codigo_operacao, nome=item.nome, tipo=item.tipo.value, status=item.status.value, plano_diretor_id=item.plano_diretor_id, orgao_responsavel_id=item.orgao_responsavel_id, provincia=item.provincia, municipio=item.municipio, area_intervencao=item.area_intervencao, investimento_previsto=item.investimento_previsto, investimento_executado=item.investimento_executado, data_inicio_prevista=item.data_inicio_prevista, data_fim_prevista=item.data_fim_prevista, data_inicio_real=item.data_inicio_real, data_fim_real=item.data_fim_real, percentual_execucao=item.percentual_execucao, data_cadastro=item.data_cadastro, data_atualizacao=item.data_atualizacao, observacoes=item.observacoes)
                self._session.add(model)
            else:
                model.nome = item.nome
                model.tipo = item.tipo.value
                model.status = item.status.value
                model.plano_diretor_id = item.plano_diretor_id
                model.orgao_responsavel_id = item.orgao_responsavel_id
                model.provincia = item.provincia
                model.municipio = item.municipio
                model.area_intervencao = item.area_intervencao
                model.investimento_previsto = item.investimento_previsto
                model.investimento_executado = item.investimento_executado
                model.data_inicio_prevista = item.data_inicio_prevista
                model.data_fim_prevista = item.data_fim_prevista
                model.data_inicio_real = item.data_inicio_real
                model.data_fim_real = item.data_fim_real
                model.percentual_execucao = item.percentual_execucao
                model.data_cadastro = item.data_cadastro
                model.data_atualizacao = item.data_atualizacao
                model.observacoes = item.observacoes
            await self._session.flush()
            return self._to_domain(model)
        self._items[item.codigo_operacao] = item
        return item

    async def get_by_codigo(self, codigo_operacao: str) -> OperacaoUrbana | None:
        if self._session:
            result = await self._session.execute(select(OperacaoUrbanaModel).where(OperacaoUrbanaModel.codigo_operacao == codigo_operacao))
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        return self._items.get(codigo_operacao)

    async def list(self, *, status: StatusOperacaoUrbana | None=None, tipo: TipoOperacaoUrbana | None=None, provincia: str | None=None) -> list[OperacaoUrbana]:
        if self._session:
            statement = select(OperacaoUrbanaModel)
            if status:
                statement = statement.where(OperacaoUrbanaModel.status == status.value)
            if tipo:
                statement = statement.where(OperacaoUrbanaModel.tipo == tipo.value)
            if provincia:
                statement = statement.where(func.lower(OperacaoUrbanaModel.provincia) == provincia.strip().lower())
            result = await self._session.execute(statement.order_by(OperacaoUrbanaModel.codigo_operacao.asc()))
            return [self._to_domain(model) for model in result.scalars().all()]
        values = list(self._items.values())
        if status:
            values = [item for item in values if item.status == status]
        if tipo:
            values = [item for item in values if item.tipo == tipo]
        if provincia:
            values = [item for item in values if item.provincia.lower() == provincia.lower()]
        return values

    async def next_codigo(self) -> str:
        if self._session:
            year = date.today().year
            prefix = f'OPU/{year}/'
            result = await self._session.execute(select(func.count()).select_from(OperacaoUrbanaModel).where(OperacaoUrbanaModel.codigo_operacao.like(f'{prefix}%')))
            seq = int(result.scalar() or 0) + 1
            return f'{prefix}{seq:06d}'
        self._seq += 1
        return f'OPU/{date.today().year}/{self._seq:06d}'

    @staticmethod
    def _to_domain(model: OperacaoUrbanaModel) -> OperacaoUrbana:
        return OperacaoUrbana(id=model.id, codigo_operacao=model.codigo_operacao, nome=model.nome, tipo=TipoOperacaoUrbana(model.tipo), status=StatusOperacaoUrbana(model.status), plano_diretor_id=model.plano_diretor_id, orgao_responsavel_id=model.orgao_responsavel_id, provincia=model.provincia, municipio=model.municipio, area_intervencao=Decimal(model.area_intervencao) if model.area_intervencao is not None else None, investimento_previsto=Decimal(model.investimento_previsto) if model.investimento_previsto is not None else None, investimento_executado=Decimal(model.investimento_executado) if model.investimento_executado is not None else None, data_inicio_prevista=model.data_inicio_prevista, data_fim_prevista=model.data_fim_prevista, data_inicio_real=model.data_inicio_real, data_fim_real=model.data_fim_real, percentual_execucao=Decimal(model.percentual_execucao), data_cadastro=model.data_cadastro, data_atualizacao=model.data_atualizacao, observacoes=model.observacoes)