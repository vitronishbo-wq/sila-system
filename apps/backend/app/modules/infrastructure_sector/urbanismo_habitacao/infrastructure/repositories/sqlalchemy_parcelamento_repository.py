from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.parcelamento_repository_port import (
    ParcelamentoRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import (
    StatusParcelamento,
    TipoParcelamento,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.parcelamento import (
    Parcelamento,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.parcelamento_model import (
    ParcelamentoModel,
)


class SQLAlchemyParcelamentoRepository(ParcelamentoRepositoryPort):
    """Repository com ORM real (AsyncSession) e fallback em memoria."""

    def __init__(self, session: AsyncSession | None = None) -> None:
        self._session = session
        self._items: dict[str, Parcelamento] = {}
        self._seq = 0

    async def save(self, item: Parcelamento) -> Parcelamento:
        if self._session:
            existing = await self._session.execute(
                select(ParcelamentoModel).where(
                    ParcelamentoModel.codigo_parcelamento == item.codigo_parcelamento
                )
            )
            model = existing.scalars().first()
            if model is None:
                model = ParcelamentoModel(
                    id=item.id,
                    codigo_parcelamento=item.codigo_parcelamento,
                    nome=item.nome,
                    tipo=item.tipo.value,
                    status=item.status.value,
                    plano_diretor_id=item.plano_diretor_id,
                    zoneamento_id=item.zoneamento_id,
                    provincia=item.provincia,
                    area_total=item.area_total,
                    quantidade_unidades_prevista=item.quantidade_unidades_prevista,
                    municipio=item.municipio,
                    area_publica_prevista=item.area_publica_prevista,
                    area_sistema_viario_prevista=item.area_sistema_viario_prevista,
                    quantidade_unidades_resultante=item.quantidade_unidades_resultante,
                    data_cadastro=item.data_cadastro,
                    data_atualizacao=item.data_atualizacao,
                    observacoes=item.observacoes,
                )
                self._session.add(model)
            else:
                model.nome = item.nome
                model.tipo = item.tipo.value
                model.status = item.status.value
                model.plano_diretor_id = item.plano_diretor_id
                model.zoneamento_id = item.zoneamento_id
                model.provincia = item.provincia
                model.area_total = item.area_total
                model.quantidade_unidades_prevista = item.quantidade_unidades_prevista
                model.municipio = item.municipio
                model.area_publica_prevista = item.area_publica_prevista
                model.area_sistema_viario_prevista = item.area_sistema_viario_prevista
                model.quantidade_unidades_resultante = item.quantidade_unidades_resultante
                model.data_cadastro = item.data_cadastro
                model.data_atualizacao = item.data_atualizacao
                model.observacoes = item.observacoes
            await self._session.flush()
            return self._to_domain(model)
        self._items[item.codigo_parcelamento] = item
        return item

    async def get_by_codigo(self, codigo_parcelamento: str) -> Parcelamento | None:
        if self._session:
            result = await self._session.execute(
                select(ParcelamentoModel).where(
                    ParcelamentoModel.codigo_parcelamento == codigo_parcelamento
                )
            )
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        return self._items.get(codigo_parcelamento)

    async def list(
        self,
        *,
        status: StatusParcelamento | None = None,
        tipo: TipoParcelamento | None = None,
        provincia: str | None = None,
    ) -> list[Parcelamento]:
        if self._session:
            statement = select(ParcelamentoModel)
            if status:
                statement = statement.where(ParcelamentoModel.status == status.value)
            if tipo:
                statement = statement.where(ParcelamentoModel.tipo == tipo.value)
            if provincia:
                statement = statement.where(
                    func.lower(ParcelamentoModel.provincia) == provincia.strip().lower()
                )
            result = await self._session.execute(
                statement.order_by(ParcelamentoModel.codigo_parcelamento.asc())
            )
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
            prefix = f"PAR/{year}/"
            result = await self._session.execute(
                select(func.count())
                .select_from(ParcelamentoModel)
                .where(ParcelamentoModel.codigo_parcelamento.like(f"{prefix}%"))
            )
            seq = int(result.scalar() or 0) + 1
            return f"{prefix}{seq:06d}"
        self._seq += 1
        return f"PAR/{date.today().year}/{self._seq:06d}"

    @staticmethod
    def _to_domain(model: ParcelamentoModel) -> Parcelamento:
        return Parcelamento(
            id=model.id,
            codigo_parcelamento=model.codigo_parcelamento,
            nome=model.nome,
            tipo=TipoParcelamento(model.tipo),
            status=StatusParcelamento(model.status),
            plano_diretor_id=model.plano_diretor_id,
            zoneamento_id=model.zoneamento_id,
            provincia=model.provincia,
            area_total=Decimal(model.area_total),
            quantidade_unidades_prevista=model.quantidade_unidades_prevista,
            municipio=model.municipio,
            area_publica_prevista=Decimal(model.area_publica_prevista)
            if model.area_publica_prevista is not None
            else None,
            area_sistema_viario_prevista=Decimal(model.area_sistema_viario_prevista)
            if model.area_sistema_viario_prevista is not None
            else None,
            quantidade_unidades_resultante=model.quantidade_unidades_resultante,
            data_cadastro=model.data_cadastro,
            data_atualizacao=model.data_atualizacao,
            observacoes=model.observacoes,
        )
