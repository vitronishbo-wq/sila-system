from __future__ import annotations
from datetime import date
from decimal import Decimal
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.ports.oneracao_repository_port import OneracaoRepositoryPort
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import StatusOneracao
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.models.oneracao import Oneracao
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import TipoOneracao
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.models.oneracao_model import OneracaoModel

class SQLAlchemyOneracaoRepository(OneracaoRepositoryPort):
    """Repository real em SQLAlchemy/AsyncSession com fallback in-memory."""

    def __init__(self, session: AsyncSession | None=None) -> None:
        self._session = session
        self._items: dict[str, Oneracao] = {}
        self._seq = 0

    async def save(self, item: Oneracao) -> Oneracao:
        if self._session:
            existing = await self._session.execute(select(OneracaoModel).where(OneracaoModel.numero_oneracao == item.numero_oneracao))
            model = existing.scalars().first()
            if model is None:
                model = OneracaoModel(id=item.id, numero_oneracao=item.numero_oneracao, imovel_inscricao=item.imovel_inscricao, tipo=item.tipo.value, credor_nome=item.credor_nome, valor=item.valor, data_registro=item.data_registro, status=item.status.value, ativo=item.ativo, documento_credor=item.documento_credor, moeda=item.moeda, data_vencimento=item.data_vencimento, descricao=item.descricao, data_atualizacao=item.data_atualizacao, observacoes=item.observacoes)
                self._session.add(model)
            else:
                model.imovel_inscricao = item.imovel_inscricao
                model.tipo = item.tipo.value
                model.credor_nome = item.credor_nome
                model.valor = item.valor
                model.status = item.status.value
                model.ativo = item.ativo
                model.documento_credor = item.documento_credor
                model.moeda = item.moeda
                model.data_vencimento = item.data_vencimento
                model.descricao = item.descricao
                model.data_atualizacao = item.data_atualizacao
                model.observacoes = item.observacoes
            await self._session.flush()
            return self._to_domain(model)
        self._items[item.numero_oneracao] = item
        return item

    async def get_by_numero(self, numero_oneracao: str) -> Oneracao | None:
        if self._session:
            result = await self._session.execute(select(OneracaoModel).where(OneracaoModel.numero_oneracao == numero_oneracao))
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        return self._items.get(numero_oneracao)

    async def list(self, *, imovel_inscricao: str | None=None, status: StatusOneracao | None=None, ativo: bool | None=None) -> list[Oneracao]:
        if self._session:
            statement = select(OneracaoModel)
            if imovel_inscricao:
                statement = statement.where(OneracaoModel.imovel_inscricao == imovel_inscricao.strip())
            if status:
                statement = statement.where(OneracaoModel.status == status.value)
            if ativo is not None:
                statement = statement.where(OneracaoModel.ativo == ativo)
            result = await self._session.execute(statement.order_by(OneracaoModel.numero_oneracao.asc()))
            return [self._to_domain(model) for model in result.scalars().all()]
        values = list(self._items.values())
        if imovel_inscricao:
            ref = imovel_inscricao.strip()
            values = [item for item in values if item.imovel_inscricao == ref]
        if status:
            values = [item for item in values if item.status == status]
        if ativo is not None:
            values = [item for item in values if item.ativo == ativo]
        return values

    async def next_numero(self) -> str:
        if self._session:
            year = date.today().year
            prefix = f'ONR/{year}/'
            result = await self._session.execute(select(func.count()).select_from(OneracaoModel).where(OneracaoModel.numero_oneracao.like(f'{prefix}%')))
            seq = int(result.scalar() or 0) + 1
            return f'{prefix}{seq:06d}'
        self._seq += 1
        return f'ONR/{date.today().year}/{self._seq:06d}'

    @staticmethod
    def _to_domain(model: OneracaoModel) -> Oneracao:
        return Oneracao(id=model.id, numero_oneracao=model.numero_oneracao, imovel_inscricao=model.imovel_inscricao, tipo=TipoOneracao(model.tipo), credor_nome=model.credor_nome, valor=Decimal(model.valor), data_registro=model.data_registro, status=StatusOneracao(model.status), ativo=model.ativo, documento_credor=model.documento_credor, moeda=model.moeda, data_vencimento=model.data_vencimento, descricao=model.descricao, data_atualizacao=model.data_atualizacao, observacoes=model.observacoes)