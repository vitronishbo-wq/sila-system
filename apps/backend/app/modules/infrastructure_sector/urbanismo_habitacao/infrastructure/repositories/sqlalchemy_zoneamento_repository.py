from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.zoneamento_repository_port import (
    ZoneamentoRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import (
    StatusZoneamento,
    TipoZona,
    UsoPermitido,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.zoneamento import (
    Zoneamento,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.zoneamento_model import (
    ZoneamentoModel,
)


class SQLAlchemyZoneamentoRepository(ZoneamentoRepositoryPort):
    """Repository com ORM real (AsyncSession) e fallback em memoria."""

    def __init__(self, session: AsyncSession | None = None) -> None:
        self._session = session
        self._items: dict[str, Zoneamento] = {}
        self._seq = 0

    async def save(self, item: Zoneamento) -> Zoneamento:
        if self._session:
            existing = await self._session.execute(
                select(ZoneamentoModel).where(
                    ZoneamentoModel.codigo_zoneamento == item.codigo_zoneamento
                )
            )
            model = existing.scalars().first()
            if model is None:
                model = ZoneamentoModel(
                    id=item.id,
                    codigo_zoneamento=item.codigo_zoneamento,
                    nome=item.nome,
                    tipo_zona=item.tipo_zona.value,
                    status=item.status.value,
                    plano_diretor_id=item.plano_diretor_id,
                    provincia=item.provincia,
                    usos_permitidos=[uso.value for uso in item.usos_permitidos],
                    municipio=item.municipio,
                    coeficiente_aproveitamento_max=item.coeficiente_aproveitamento_max,
                    taxa_ocupacao_max=item.taxa_ocupacao_max,
                    gabarito_maximo=item.gabarito_maximo,
                    recuo_frontal_minimo=item.recuo_frontal_minimo,
                    permeabilidade_minima=item.permeabilidade_minima,
                    area_lote_minima=item.area_lote_minima,
                    data_inicio_vigencia=item.data_inicio_vigencia,
                    data_cadastro=item.data_cadastro,
                    data_atualizacao=item.data_atualizacao,
                    observacoes=item.observacoes,
                )
                self._session.add(model)
            else:
                model.nome = item.nome
                model.tipo_zona = item.tipo_zona.value
                model.status = item.status.value
                model.plano_diretor_id = item.plano_diretor_id
                model.provincia = item.provincia
                model.usos_permitidos = [uso.value for uso in item.usos_permitidos]
                model.municipio = item.municipio
                model.coeficiente_aproveitamento_max = item.coeficiente_aproveitamento_max
                model.taxa_ocupacao_max = item.taxa_ocupacao_max
                model.gabarito_maximo = item.gabarito_maximo
                model.recuo_frontal_minimo = item.recuo_frontal_minimo
                model.permeabilidade_minima = item.permeabilidade_minima
                model.area_lote_minima = item.area_lote_minima
                model.data_inicio_vigencia = item.data_inicio_vigencia
                model.data_cadastro = item.data_cadastro
                model.data_atualizacao = item.data_atualizacao
                model.observacoes = item.observacoes
            await self._session.flush()
            return self._to_domain(model)
        self._items[item.codigo_zoneamento] = item
        return item

    async def get_by_codigo(self, codigo_zoneamento: str) -> Zoneamento | None:
        if self._session:
            result = await self._session.execute(
                select(ZoneamentoModel).where(
                    ZoneamentoModel.codigo_zoneamento == codigo_zoneamento
                )
            )
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        return self._items.get(codigo_zoneamento)

    async def list(
        self,
        *,
        status: StatusZoneamento | None = None,
        tipo_zona: TipoZona | None = None,
        provincia: str | None = None,
    ) -> list[Zoneamento]:
        if self._session:
            statement = select(ZoneamentoModel)
            if status:
                statement = statement.where(ZoneamentoModel.status == status.value)
            if tipo_zona:
                statement = statement.where(ZoneamentoModel.tipo_zona == tipo_zona.value)
            if provincia:
                statement = statement.where(
                    func.lower(ZoneamentoModel.provincia) == provincia.strip().lower()
                )
            result = await self._session.execute(
                statement.order_by(ZoneamentoModel.codigo_zoneamento.asc())
            )
            return [self._to_domain(model) for model in result.scalars().all()]
        values = list(self._items.values())
        if status:
            values = [item for item in values if item.status == status]
        if tipo_zona:
            values = [item for item in values if item.tipo_zona == tipo_zona]
        if provincia:
            values = [item for item in values if item.provincia.lower() == provincia.lower()]
        return values

    async def next_codigo(self) -> str:
        if self._session:
            year = date.today().year
            prefix = f"ZON/{year}/"
            result = await self._session.execute(
                select(func.count())
                .select_from(ZoneamentoModel)
                .where(ZoneamentoModel.codigo_zoneamento.like(f"{prefix}%"))
            )
            seq = int(result.scalar() or 0) + 1
            return f"{prefix}{seq:06d}"
        self._seq += 1
        return f"ZON/{date.today().year}/{self._seq:06d}"

    @staticmethod
    def _to_domain(model: ZoneamentoModel) -> Zoneamento:
        usos_permitidos = [UsoPermitido(value) for value in model.usos_permitidos or []]
        return Zoneamento(
            id=model.id,
            codigo_zoneamento=model.codigo_zoneamento,
            nome=model.nome,
            tipo_zona=TipoZona(model.tipo_zona),
            status=StatusZoneamento(model.status),
            plano_diretor_id=model.plano_diretor_id,
            provincia=model.provincia,
            usos_permitidos=usos_permitidos,
            municipio=model.municipio,
            coeficiente_aproveitamento_max=Decimal(model.coeficiente_aproveitamento_max)
            if model.coeficiente_aproveitamento_max is not None
            else None,
            taxa_ocupacao_max=Decimal(model.taxa_ocupacao_max)
            if model.taxa_ocupacao_max is not None
            else None,
            gabarito_maximo=model.gabarito_maximo,
            recuo_frontal_minimo=Decimal(model.recuo_frontal_minimo)
            if model.recuo_frontal_minimo is not None
            else None,
            permeabilidade_minima=Decimal(model.permeabilidade_minima)
            if model.permeabilidade_minima is not None
            else None,
            area_lote_minima=Decimal(model.area_lote_minima)
            if model.area_lote_minima is not None
            else None,
            data_inicio_vigencia=model.data_inicio_vigencia,
            data_cadastro=model.data_cadastro,
            data_atualizacao=model.data_atualizacao,
            observacoes=model.observacoes,
        )
