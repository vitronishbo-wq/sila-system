from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.resources.pescas.application.ports import CapturaRepositoryPort
from apps.backend.app.modules.resources.pescas.domain.models.captura import Captura
from apps.backend.app.modules.resources.pescas.infrastructure.models.captura_model import (
    CapturaModel,
)


class SQLAlchemyCapturaRepository(CapturaRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, captura: Captura) -> Captura:
        model = await self.session.get(CapturaModel, captura.id)
        if not model:
            model = CapturaModel(id=captura.id)
            self.session.add(model)
        model.embarcacao_id = captura.embarcacao_id
        model.licenca_id = captura.licenca_id
        model.data_inicio = captura.data_inicio
        model.data_fim = captura.data_fim
        model.zona_pesca_id = captura.zona_pesca_id
        model.especie_id = captura.especie_id
        model.quantidade_kg = captura.quantidade_kg
        model.quantidade_unidades = captura.quantidade_unidades
        model.arte_pesca_id = captura.arte_pesca_id
        model.profundidade = captura.profundidade
        model.coordenadas_inicio = captura.coordenadas_inicio
        model.coordenadas_fim = captura.coordenadas_fim
        model.condicoes_mar = captura.condicoes_mar
        model.observacoes = captura.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, captura_id: UUID) -> Captura | None:
        model = await self.session.get(CapturaModel, captura_id)
        return self._to_domain(model) if model else None

    async def list_by_embarcacao(self, embarcacao_id: UUID) -> list[Captura]:
        stmt = select(CapturaModel).where(CapturaModel.embarcacao_id == embarcacao_id)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def list_by_licenca(self, licenca_id: UUID) -> list[Captura]:
        stmt = select(CapturaModel).where(CapturaModel.licenca_id == licenca_id)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def list_by_periodo(self, data_inicio: datetime, data_fim: datetime) -> list[Captura]:
        stmt = select(CapturaModel).where(
            CapturaModel.data_inicio >= data_inicio, CapturaModel.data_fim <= data_fim
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    @staticmethod
    def _to_domain(model: CapturaModel) -> Captura:
        return Captura(
            id=model.id,
            embarcacao_id=model.embarcacao_id,
            licenca_id=model.licenca_id,
            data_inicio=model.data_inicio,
            data_fim=model.data_fim,
            zona_pesca_id=model.zona_pesca_id,
            especie_id=model.especie_id,
            quantidade_kg=model.quantidade_kg,
            quantidade_unidades=model.quantidade_unidades,
            arte_pesca_id=model.arte_pesca_id,
            profundidade=model.profundidade,
            coordenadas_inicio=model.coordenadas_inicio,
            coordenadas_fim=model.coordenadas_fim,
            condicoes_mar=model.condicoes_mar,
            observacoes=model.observacoes,
        )
