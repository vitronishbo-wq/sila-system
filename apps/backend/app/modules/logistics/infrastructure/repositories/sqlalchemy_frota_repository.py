from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.logistics.domain.enums import StatusFrota
from apps.backend.app.modules.logistics.domain.models import Frota
from apps.backend.app.modules.logistics.domain.ports import FrotaRepositoryPort
from apps.backend.app.modules.logistics.infrastructure.orm import FrotaModel


class SQLAlchemyFrotaRepository(FrotaRepositoryPort):
    """Repository com ORM real (AsyncSession) e fallback em memoria."""

    def __init__(self, session: AsyncSession | None = None) -> None:
        self._session = session
        self._items: dict[str, Frota] = {}
        self._seq = 0

    async def save(self, item: Frota) -> Frota:
        if self._session:
            existing = await self._session.execute(
                select(FrotaModel).where(FrotaModel.codigo_frota == item.codigo_frota)
            )
            model = existing.scalars().first()
            if model is None:
                model = FrotaModel(
                    id=item.id,
                    codigo_frota=item.codigo_frota,
                    nome=item.nome,
                    operadora_id=item.operadora_id,
                    municipio=item.municipio,
                    provincia=item.provincia,
                    status=item.status.value,
                    data_cadastro=item.data_cadastro,
                    data_atualizacao=item.data_atualizacao,
                    observacoes=item.observacoes,
                    veiculos=item.veiculos,
                    manutencoes=item.manutencoes,
                    fiscalizacoes=item.fiscalizacoes,
                    tarifas=item.tarifas,
                    trilha_auditoria=item.trilha_auditoria,
                )
                self._session.add(model)
            else:
                model.nome = item.nome
                model.operadora_id = item.operadora_id
                model.municipio = item.municipio
                model.provincia = item.provincia
                model.status = item.status.value
                model.data_cadastro = item.data_cadastro
                model.data_atualizacao = item.data_atualizacao
                model.observacoes = item.observacoes
                model.veiculos = item.veiculos
                model.manutencoes = item.manutencoes
                model.fiscalizacoes = item.fiscalizacoes
                model.tarifas = item.tarifas
                model.trilha_auditoria = item.trilha_auditoria
            await self._session.flush()
            return self._to_domain(model)
        self._items[item.codigo_frota] = item
        return item

    async def get_by_codigo(self, codigo_frota: str) -> Frota | None:
        if self._session:
            result = await self._session.execute(
                select(FrotaModel).where(FrotaModel.codigo_frota == codigo_frota)
            )
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        return self._items.get(codigo_frota)

    async def list(
        self,
        *,
        status: StatusFrota | None = None,
        operadora_id: UUID | None = None,
        municipio: str | None = None,
        provincia: str | None = None,
    ) -> list[Frota]:
        if self._session:
            statement = select(FrotaModel)
            if status:
                statement = statement.where(FrotaModel.status == status.value)
            if operadora_id:
                statement = statement.where(FrotaModel.operadora_id == operadora_id)
            if municipio:
                statement = statement.where(
                    func.lower(FrotaModel.municipio) == municipio.strip().lower()
                )
            if provincia:
                statement = statement.where(
                    func.lower(FrotaModel.provincia) == provincia.strip().lower()
                )
            result = await self._session.execute(statement.order_by(FrotaModel.codigo_frota.asc()))
            return [self._to_domain(model) for model in result.scalars().all()]
        values = list(self._items.values())
        if status:
            values = [item for item in values if item.status == status]
        if operadora_id:
            values = [item for item in values if item.operadora_id == operadora_id]
        if municipio:
            muni = municipio.strip().lower()
            values = [item for item in values if item.municipio.lower() == muni]
        if provincia:
            prov = provincia.strip().lower()
            values = [item for item in values if item.provincia.lower() == prov]
        return values

    async def next_codigo(self) -> str:
        if self._session:
            year = date.today().year
            prefix = f"FRT/{year}/"
            result = await self._session.execute(
                select(func.count())
                .select_from(FrotaModel)
                .where(FrotaModel.codigo_frota.like(f"{prefix}%"))
            )
            seq = int(result.scalar() or 0) + 1
            return f"{prefix}{seq:06d}"
        self._seq += 1
        return f"FRT/{date.today().year}/{self._seq:06d}"

    @staticmethod
    def _to_domain(model: FrotaModel) -> Frota:
        return Frota(
            id=model.id,
            codigo_frota=model.codigo_frota,
            nome=model.nome,
            operadora_id=model.operadora_id,
            municipio=model.municipio,
            provincia=model.provincia,
            status=StatusFrota(model.status),
            data_cadastro=model.data_cadastro,
            data_atualizacao=model.data_atualizacao,
            observacoes=model.observacoes,
            veiculos=list(model.veiculos or []),
            manutencoes=list(model.manutencoes or []),
            fiscalizacoes=list(model.fiscalizacoes or []),
            tarifas=list(model.tarifas or []),
            trilha_auditoria=list(model.trilha_auditoria or []),
        )
