from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.infrastructure.application.ports.licitacao_repository_port import (
    LicitacaoRepositoryPort,
)
from apps.backend.app.modules.infrastructure.domain.enums import StatusLicitacao, TipoLicitacao
from apps.backend.app.modules.infrastructure.domain.models.licitacao import Licitacao
from apps.backend.app.modules.infrastructure.infrastructure.models.licitacao_model import (
    LicitacaoModel,
)


class SQLAlchemyLicitacaoRepository(LicitacaoRepositoryPort):
    """Repository com ORM real (AsyncSession) e fallback em memoria."""

    def __init__(self, session: AsyncSession | None = None) -> None:
        self._session = session
        self._items: dict[str, Licitacao] = {}
        self._seq = 0

    async def save(self, item: Licitacao) -> Licitacao:
        if self._session:
            existing = await self._session.execute(
                select(LicitacaoModel).where(
                    LicitacaoModel.numero_licitacao == item.numero_licitacao
                )
            )
            model = existing.scalars().first()
            if model is None:
                model = LicitacaoModel(
                    id=item.id,
                    numero_licitacao=item.numero_licitacao,
                    objeto=item.objeto,
                    tipo=item.tipo.value,
                    status=item.status.value,
                    obra_id=item.obra_id,
                    orgao_responsavel_id=item.orgao_responsavel_id,
                    valor_estimado=item.valor_estimado,
                    data_publicacao_edital=item.data_publicacao_edital,
                    data_entrega_propostas=item.data_entrega_propostas,
                    data_cadastro=item.data_cadastro,
                    data_abertura=item.data_abertura,
                    vencedor_id=item.vencedor_id,
                    valor_adjudicado=item.valor_adjudicado,
                    data_homologacao=item.data_homologacao,
                    data_atualizacao=item.data_atualizacao,
                    observacoes=item.observacoes,
                )
                self._session.add(model)
            else:
                model.objeto = item.objeto
                model.tipo = item.tipo.value
                model.status = item.status.value
                model.obra_id = item.obra_id
                model.orgao_responsavel_id = item.orgao_responsavel_id
                model.valor_estimado = item.valor_estimado
                model.data_publicacao_edital = item.data_publicacao_edital
                model.data_entrega_propostas = item.data_entrega_propostas
                model.data_cadastro = item.data_cadastro
                model.data_abertura = item.data_abertura
                model.vencedor_id = item.vencedor_id
                model.valor_adjudicado = item.valor_adjudicado
                model.data_homologacao = item.data_homologacao
                model.data_atualizacao = item.data_atualizacao
                model.observacoes = item.observacoes
            await self._session.flush()
            return self._to_domain(model)
        self._items[item.numero_licitacao] = item
        return item

    async def get_by_numero(self, numero_licitacao: str) -> Licitacao | None:
        if self._session:
            result = await self._session.execute(
                select(LicitacaoModel).where(LicitacaoModel.numero_licitacao == numero_licitacao)
            )
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        return self._items.get(numero_licitacao)

    async def list(
        self,
        *,
        status: StatusLicitacao | None = None,
        tipo: TipoLicitacao | None = None,
        obra_id: UUID | None = None,
        orgao_responsavel_id: UUID | None = None,
    ) -> list[Licitacao]:
        if self._session:
            statement = select(LicitacaoModel)
            if status:
                statement = statement.where(LicitacaoModel.status == status.value)
            if tipo:
                statement = statement.where(LicitacaoModel.tipo == tipo.value)
            if obra_id:
                statement = statement.where(LicitacaoModel.obra_id == obra_id)
            if orgao_responsavel_id:
                statement = statement.where(
                    LicitacaoModel.orgao_responsavel_id == orgao_responsavel_id
                )
            result = await self._session.execute(
                statement.order_by(LicitacaoModel.numero_licitacao.asc())
            )
            return [self._to_domain(model) for model in result.scalars().all()]
        values = list(self._items.values())
        if status:
            values = [item for item in values if item.status == status]
        if tipo:
            values = [item for item in values if item.tipo == tipo]
        if obra_id:
            values = [item for item in values if item.obra_id == obra_id]
        if orgao_responsavel_id:
            values = [item for item in values if item.orgao_responsavel_id == orgao_responsavel_id]
        return values

    async def next_numero(self) -> str:
        if self._session:
            year = date.today().year
            prefix = f"LIC/{year}/"
            result = await self._session.execute(
                select(func.count())
                .select_from(LicitacaoModel)
                .where(LicitacaoModel.numero_licitacao.like(f"{prefix}%"))
            )
            seq = int(result.scalar() or 0) + 1
            return f"{prefix}{seq:06d}"
        self._seq += 1
        return f"LIC/{date.today().year}/{self._seq:06d}"

    @staticmethod
    def _to_domain(model: LicitacaoModel) -> Licitacao:
        return Licitacao(
            id=model.id,
            numero_licitacao=model.numero_licitacao,
            objeto=model.objeto,
            tipo=TipoLicitacao(model.tipo),
            status=StatusLicitacao(model.status),
            obra_id=model.obra_id,
            orgao_responsavel_id=model.orgao_responsavel_id,
            valor_estimado=Decimal(model.valor_estimado),
            data_publicacao_edital=model.data_publicacao_edital,
            data_entrega_propostas=model.data_entrega_propostas,
            data_cadastro=model.data_cadastro,
            data_abertura=model.data_abertura,
            vencedor_id=model.vencedor_id,
            valor_adjudicado=Decimal(model.valor_adjudicado)
            if model.valor_adjudicado is not None
            else None,
            data_homologacao=model.data_homologacao,
            data_atualizacao=model.data_atualizacao,
            observacoes=model.observacoes,
        )
