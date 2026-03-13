from __future__ import annotations
from datetime import date
from decimal import Decimal
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.loteamento_repository_port import LoteamentoRepositoryPort
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusLoteamento, TipoLoteamento
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.loteamento import Loteamento
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.loteamento_model import LoteamentoModel

class SQLAlchemyLoteamentoRepository(LoteamentoRepositoryPort):
    """Repository com ORM real (AsyncSession) e fallback em memoria."""

    def __init__(self, session: AsyncSession | None=None) -> None:
        self._session = session
        self._items: dict[str, Loteamento] = {}
        self._seq = 0

    async def save(self, item: Loteamento) -> Loteamento:
        if self._session:
            existing = await self._session.execute(select(LoteamentoModel).where(LoteamentoModel.codigo_loteamento == item.codigo_loteamento))
            model = existing.scalars().first()
            if model is None:
                model = LoteamentoModel(id=item.id, codigo_loteamento=item.codigo_loteamento, nome=item.nome, tipo=item.tipo.value, status=item.status.value, parcelamento_id=item.parcelamento_id, plano_diretor_id=item.plano_diretor_id, zoneamento_id=item.zoneamento_id, provincia=item.provincia, area_total=item.area_total, quantidade_lotes_prevista=item.quantidade_lotes_prevista, municipio=item.municipio, quantidade_lotes_implantada=item.quantidade_lotes_implantada, area_lotes=item.area_lotes, area_verde=item.area_verde, area_institucional=item.area_institucional, data_inicio_prevista=item.data_inicio_prevista, data_fim_prevista=item.data_fim_prevista, data_inicio_real=item.data_inicio_real, data_fim_real=item.data_fim_real, data_cadastro=item.data_cadastro, data_atualizacao=item.data_atualizacao, observacoes=item.observacoes)
                self._session.add(model)
            else:
                model.nome = item.nome
                model.tipo = item.tipo.value
                model.status = item.status.value
                model.parcelamento_id = item.parcelamento_id
                model.plano_diretor_id = item.plano_diretor_id
                model.zoneamento_id = item.zoneamento_id
                model.provincia = item.provincia
                model.area_total = item.area_total
                model.quantidade_lotes_prevista = item.quantidade_lotes_prevista
                model.municipio = item.municipio
                model.quantidade_lotes_implantada = item.quantidade_lotes_implantada
                model.area_lotes = item.area_lotes
                model.area_verde = item.area_verde
                model.area_institucional = item.area_institucional
                model.data_inicio_prevista = item.data_inicio_prevista
                model.data_fim_prevista = item.data_fim_prevista
                model.data_inicio_real = item.data_inicio_real
                model.data_fim_real = item.data_fim_real
                model.data_cadastro = item.data_cadastro
                model.data_atualizacao = item.data_atualizacao
                model.observacoes = item.observacoes
            await self._session.flush()
            return self._to_domain(model)
        self._items[item.codigo_loteamento] = item
        return item

    async def get_by_codigo(self, codigo_loteamento: str) -> Loteamento | None:
        if self._session:
            result = await self._session.execute(select(LoteamentoModel).where(LoteamentoModel.codigo_loteamento == codigo_loteamento))
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        return self._items.get(codigo_loteamento)

    async def list(self, *, status: StatusLoteamento | None=None, tipo: TipoLoteamento | None=None, provincia: str | None=None) -> list[Loteamento]:
        if self._session:
            statement = select(LoteamentoModel)
            if status:
                statement = statement.where(LoteamentoModel.status == status.value)
            if tipo:
                statement = statement.where(LoteamentoModel.tipo == tipo.value)
            if provincia:
                statement = statement.where(func.lower(LoteamentoModel.provincia) == provincia.strip().lower())
            result = await self._session.execute(statement.order_by(LoteamentoModel.codigo_loteamento.asc()))
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
            prefix = f'LOT/{year}/'
            result = await self._session.execute(select(func.count()).select_from(LoteamentoModel).where(LoteamentoModel.codigo_loteamento.like(f'{prefix}%')))
            seq = int(result.scalar() or 0) + 1
            return f'{prefix}{seq:06d}'
        self._seq += 1
        return f'LOT/{date.today().year}/{self._seq:06d}'

    @staticmethod
    def _to_domain(model: LoteamentoModel) -> Loteamento:
        return Loteamento(id=model.id, codigo_loteamento=model.codigo_loteamento, nome=model.nome, tipo=TipoLoteamento(model.tipo), status=StatusLoteamento(model.status), parcelamento_id=model.parcelamento_id, plano_diretor_id=model.plano_diretor_id, zoneamento_id=model.zoneamento_id, provincia=model.provincia, area_total=Decimal(model.area_total), quantidade_lotes_prevista=model.quantidade_lotes_prevista, municipio=model.municipio, quantidade_lotes_implantada=model.quantidade_lotes_implantada, area_lotes=Decimal(model.area_lotes) if model.area_lotes is not None else None, area_verde=Decimal(model.area_verde) if model.area_verde is not None else None, area_institucional=Decimal(model.area_institucional) if model.area_institucional is not None else None, data_inicio_prevista=model.data_inicio_prevista, data_fim_prevista=model.data_fim_prevista, data_inicio_real=model.data_inicio_real, data_fim_real=model.data_fim_real, data_cadastro=model.data_cadastro, data_atualizacao=model.data_atualizacao, observacoes=model.observacoes)