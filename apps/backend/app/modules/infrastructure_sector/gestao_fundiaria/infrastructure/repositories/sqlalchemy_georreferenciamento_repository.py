from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.ports.georreferenciamento_repository_port import (
    GeorreferenciamentoRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.models.georreferenciamento import (
    Georreferenciamento,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.models.georreferenciamento_model import (
    GeorreferenciamentoModel,
)


class SQLAlchemyGeorreferenciamentoRepository(GeorreferenciamentoRepositoryPort):
    def __init__(self, session: AsyncSession | None = None) -> None:
        self._session = session
        self._items: dict[str, Georreferenciamento] = {}
        self._seq = 0

    async def save(self, item: Georreferenciamento) -> Georreferenciamento:
        if self._session:
            existing = await self._session.execute(
                select(GeorreferenciamentoModel).where(
                    GeorreferenciamentoModel.codigo_geo == item.codigo_geo
                )
            )
            model = existing.scalars().first()
            if model is None:
                model = GeorreferenciamentoModel(
                    id=item.id,
                    codigo_geo=item.codigo_geo,
                    imovel_inscricao=item.imovel_inscricao,
                    latitude=item.latitude,
                    longitude=item.longitude,
                    sistema_referencia=item.sistema_referencia,
                    data_registro=item.data_registro,
                    precisao_metros=item.precisao_metros,
                    area_calculada=item.area_calculada,
                    validado=item.validado,
                    ativo=item.ativo,
                    data_atualizacao=item.data_atualizacao,
                    observacoes=item.observacoes,
                )
                self._session.add(model)
            else:
                model.imovel_inscricao = item.imovel_inscricao
                model.latitude = item.latitude
                model.longitude = item.longitude
                model.sistema_referencia = item.sistema_referencia
                model.precisao_metros = item.precisao_metros
                model.area_calculada = item.area_calculada
                model.validado = item.validado
                model.ativo = item.ativo
                model.data_atualizacao = item.data_atualizacao
                model.observacoes = item.observacoes
            await self._session.flush()
            return self._to_domain(model)
        self._items[item.codigo_geo] = item
        return item

    async def get_by_codigo(self, codigo_geo: str) -> Georreferenciamento | None:
        if self._session:
            result = await self._session.execute(
                select(GeorreferenciamentoModel).where(
                    GeorreferenciamentoModel.codigo_geo == codigo_geo
                )
            )
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        return self._items.get(codigo_geo)

    async def list(
        self,
        *,
        imovel_inscricao: str | None = None,
        validado: bool | None = None,
        ativo: bool | None = None,
    ) -> list[Georreferenciamento]:
        if self._session:
            statement = select(GeorreferenciamentoModel)
            if imovel_inscricao:
                statement = statement.where(
                    GeorreferenciamentoModel.imovel_inscricao == imovel_inscricao.strip()
                )
            if validado is not None:
                statement = statement.where(GeorreferenciamentoModel.validado == validado)
            if ativo is not None:
                statement = statement.where(GeorreferenciamentoModel.ativo == ativo)
            result = await self._session.execute(
                statement.order_by(GeorreferenciamentoModel.codigo_geo.asc())
            )
            return [self._to_domain(model) for model in result.scalars().all()]
        values = list(self._items.values())
        if imovel_inscricao:
            values = [item for item in values if item.imovel_inscricao == imovel_inscricao.strip()]
        if validado is not None:
            values = [item for item in values if item.validado == validado]
        if ativo is not None:
            values = [item for item in values if item.ativo == ativo]
        return values

    async def next_codigo(self) -> str:
        if self._session:
            year = date.today().year
            prefix = f"GEO/{year}/"
            result = await self._session.execute(
                select(func.count())
                .select_from(GeorreferenciamentoModel)
                .where(GeorreferenciamentoModel.codigo_geo.like(f"{prefix}%"))
            )
            seq = int(result.scalar() or 0) + 1
            return f"{prefix}{seq:06d}"
        self._seq += 1
        return f"GEO/{date.today().year}/{self._seq:06d}"

    @staticmethod
    def _to_domain(model: GeorreferenciamentoModel) -> Georreferenciamento:
        return Georreferenciamento(
            id=model.id,
            codigo_geo=model.codigo_geo,
            imovel_inscricao=model.imovel_inscricao,
            latitude=Decimal(model.latitude),
            longitude=Decimal(model.longitude),
            sistema_referencia=model.sistema_referencia,
            data_registro=model.data_registro,
            precisao_metros=Decimal(model.precisao_metros)
            if model.precisao_metros is not None
            else None,
            area_calculada=Decimal(model.area_calculada)
            if model.area_calculada is not None
            else None,
            validado=model.validado,
            ativo=model.ativo,
            data_atualizacao=model.data_atualizacao,
            observacoes=model.observacoes,
        )
