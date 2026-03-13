from __future__ import annotations
from datetime import date
from decimal import Decimal
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.ports.desapropriacao_repository_port import DesapropriacaoRepositoryPort
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import StatusDesapropriacao
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.models.desapropriacao import Desapropriacao
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import TipoDesapropriacao
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.models.desapropriacao_model import DesapropriacaoModel

class SQLAlchemyDesapropriacaoRepository(DesapropriacaoRepositoryPort):
    """Repository real com AsyncSession e fallback in-memory."""

    def __init__(self, session: AsyncSession | None=None) -> None:
        self._session = session
        self._items: dict[str, Desapropriacao] = {}
        self._seq = 0

    async def save(self, item: Desapropriacao) -> Desapropriacao:
        if self._session:
            existing = await self._session.execute(select(DesapropriacaoModel).where(DesapropriacaoModel.numero_processo == item.numero_processo))
            model = existing.scalars().first()
            if model is None:
                model = DesapropriacaoModel(id=item.id, numero_processo=item.numero_processo, imovel_inscricao=item.imovel_inscricao, tipo=item.tipo.value, ente_publico=item.ente_publico, finalidade=item.finalidade, valor_indenizacao=item.valor_indenizacao, data_inicio=item.data_inicio, status=item.status.value, ativo=item.ativo, data_decreto=item.data_decreto, data_pagamento=item.data_pagamento, data_atualizacao=item.data_atualizacao, observacoes=item.observacoes)
                self._session.add(model)
            else:
                model.imovel_inscricao = item.imovel_inscricao
                model.tipo = item.tipo.value
                model.ente_publico = item.ente_publico
                model.finalidade = item.finalidade
                model.valor_indenizacao = item.valor_indenizacao
                model.status = item.status.value
                model.ativo = item.ativo
                model.data_decreto = item.data_decreto
                model.data_pagamento = item.data_pagamento
                model.data_atualizacao = item.data_atualizacao
                model.observacoes = item.observacoes
            await self._session.flush()
            return self._to_domain(model)
        self._items[item.numero_processo] = item
        return item

    async def get_by_numero_processo(self, numero_processo: str) -> Desapropriacao | None:
        if self._session:
            result = await self._session.execute(select(DesapropriacaoModel).where(DesapropriacaoModel.numero_processo == numero_processo))
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        return self._items.get(numero_processo)

    async def list(self, *, imovel_inscricao: str | None=None, status: StatusDesapropriacao | None=None, ativo: bool | None=None) -> list[Desapropriacao]:
        if self._session:
            statement = select(DesapropriacaoModel)
            if imovel_inscricao:
                statement = statement.where(DesapropriacaoModel.imovel_inscricao == imovel_inscricao.strip())
            if status:
                statement = statement.where(DesapropriacaoModel.status == status.value)
            if ativo is not None:
                statement = statement.where(DesapropriacaoModel.ativo == ativo)
            result = await self._session.execute(statement.order_by(DesapropriacaoModel.numero_processo.asc()))
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

    async def next_numero_processo(self) -> str:
        if self._session:
            year = date.today().year
            prefix = f'DSP/{year}/'
            result = await self._session.execute(select(func.count()).select_from(DesapropriacaoModel).where(DesapropriacaoModel.numero_processo.like(f'{prefix}%')))
            seq = int(result.scalar() or 0) + 1
            return f'{prefix}{seq:06d}'
        self._seq += 1
        return f'DSP/{date.today().year}/{self._seq:06d}'

    @staticmethod
    def _to_domain(model: DesapropriacaoModel) -> Desapropriacao:
        return Desapropriacao(id=model.id, numero_processo=model.numero_processo, imovel_inscricao=model.imovel_inscricao, tipo=TipoDesapropriacao(model.tipo), ente_publico=model.ente_publico, finalidade=model.finalidade, valor_indenizacao=Decimal(model.valor_indenizacao), data_inicio=model.data_inicio, status=StatusDesapropriacao(model.status), ativo=model.ativo, data_decreto=model.data_decreto, data_pagamento=model.data_pagamento, data_atualizacao=model.data_atualizacao, observacoes=model.observacoes)