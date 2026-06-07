from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.habite_se_repository_port import (
    HabiteSeRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import (
    StatusHabiteSe,
    TipoHabiteSe,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.habite_se import (
    HabiteSe,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.habite_se_model import (
    HabiteSeModel,
)


class SQLAlchemyHabiteSeRepository(HabiteSeRepositoryPort):
    """Repository com ORM real (AsyncSession) e fallback em memoria."""

    def __init__(self, session: AsyncSession | None = None) -> None:
        self._session = session
        self._items: dict[str, HabiteSe] = {}
        self._seq = 0

    async def save(self, item: HabiteSe) -> HabiteSe:
        if self._session:
            existing = await self._session.execute(
                select(HabiteSeModel).where(HabiteSeModel.codigo_habite_se == item.codigo_habite_se)
            )
            model = existing.scalars().first()
            if model is None:
                model = HabiteSeModel(
                    id=item.id,
                    codigo_habite_se=item.codigo_habite_se,
                    numero_processo=item.numero_processo,
                    tipo=item.tipo.value,
                    status=item.status.value,
                    alvara_id=item.alvara_id,
                    requerente_id=item.requerente_id,
                    provincia=item.provincia,
                    municipio=item.municipio,
                    endereco_imovel=item.endereco_imovel,
                    area_vistoriada=item.area_vistoriada,
                    data_requerimento=item.data_requerimento,
                    data_vistoria=item.data_vistoria,
                    data_emissao=item.data_emissao,
                    data_validade=item.data_validade,
                    tecnico_vistoriador_id=item.tecnico_vistoriador_id,
                    observacoes=item.observacoes,
                    data_atualizacao=item.data_atualizacao,
                )
                self._session.add(model)
            else:
                model.numero_processo = item.numero_processo
                model.tipo = item.tipo.value
                model.status = item.status.value
                model.alvara_id = item.alvara_id
                model.requerente_id = item.requerente_id
                model.provincia = item.provincia
                model.municipio = item.municipio
                model.endereco_imovel = item.endereco_imovel
                model.area_vistoriada = item.area_vistoriada
                model.data_requerimento = item.data_requerimento
                model.data_vistoria = item.data_vistoria
                model.data_emissao = item.data_emissao
                model.data_validade = item.data_validade
                model.tecnico_vistoriador_id = item.tecnico_vistoriador_id
                model.observacoes = item.observacoes
                model.data_atualizacao = item.data_atualizacao
            await self._session.flush()
            return self._to_domain(model)
        self._items[item.codigo_habite_se] = item
        return item

    async def get_by_codigo(self, codigo_habite_se: str) -> HabiteSe | None:
        if self._session:
            result = await self._session.execute(
                select(HabiteSeModel).where(HabiteSeModel.codigo_habite_se == codigo_habite_se)
            )
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        return self._items.get(codigo_habite_se)

    async def list(
        self,
        *,
        status: StatusHabiteSe | None = None,
        tipo: TipoHabiteSe | None = None,
        provincia: str | None = None,
    ) -> list[HabiteSe]:
        if self._session:
            statement = select(HabiteSeModel)
            if status:
                statement = statement.where(HabiteSeModel.status == status.value)
            if tipo:
                statement = statement.where(HabiteSeModel.tipo == tipo.value)
            if provincia:
                statement = statement.where(
                    func.lower(HabiteSeModel.provincia) == provincia.strip().lower()
                )
            result = await self._session.execute(
                statement.order_by(HabiteSeModel.codigo_habite_se.asc())
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
            prefix = f"HBT/{year}/"
            result = await self._session.execute(
                select(func.count())
                .select_from(HabiteSeModel)
                .where(HabiteSeModel.codigo_habite_se.like(f"{prefix}%"))
            )
            seq = int(result.scalar() or 0) + 1
            return f"{prefix}{seq:06d}"
        self._seq += 1
        return f"HBT/{date.today().year}/{self._seq:06d}"

    @staticmethod
    def _to_domain(model: HabiteSeModel) -> HabiteSe:
        return HabiteSe(
            id=model.id,
            codigo_habite_se=model.codigo_habite_se,
            numero_processo=model.numero_processo,
            tipo=TipoHabiteSe(model.tipo),
            status=StatusHabiteSe(model.status),
            alvara_id=model.alvara_id,
            requerente_id=model.requerente_id,
            provincia=model.provincia,
            municipio=model.municipio,
            endereco_imovel=model.endereco_imovel,
            area_vistoriada=Decimal(model.area_vistoriada)
            if model.area_vistoriada is not None
            else None,
            data_requerimento=model.data_requerimento,
            data_vistoria=model.data_vistoria,
            data_emissao=model.data_emissao,
            data_validade=model.data_validade,
            tecnico_vistoriador_id=model.tecnico_vistoriador_id,
            observacoes=model.observacoes,
            data_atualizacao=model.data_atualizacao,
        )
