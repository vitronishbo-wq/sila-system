from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.infrastructure_sector.meteorologia.application.ports.observacao_repository_port import (
    ObservacaoRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.meteorologia.domain.enums import ObservationType
from apps.backend.app.modules.infrastructure_sector.meteorologia.domain.models import (
    ObservacaoMeteorologica,
)
from apps.backend.app.modules.infrastructure_sector.meteorologia.infrastructure.models.observacao_model import (
    ObservacaoMeteorologicaModel,
)


class SQLAlchemyObservacaoRepository(ObservacaoRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, observacao: ObservacaoMeteorologica) -> ObservacaoMeteorologica:
        model = await self.session.get(ObservacaoMeteorologicaModel, observacao.id)
        if model is None:
            model = ObservacaoMeteorologicaModel(id=observacao.id)
            self.session.add(model)
        model.estacao_id = observacao.estacao_id
        model.data_observacao = observacao.data_observacao
        model.temperatura = observacao.temperatura
        model.humidade = observacao.humidade
        model.pressao = observacao.pressao
        model.velocidade_vento = observacao.velocidade_vento
        model.direcao_vento = observacao.direcao_vento
        model.precipitacao = observacao.precipitacao
        model.radiacao_solar = observacao.radiacao_solar
        model.tipo = observacao.tipo.value
        model.qualidade_dados = observacao.qualidade_dados
        model.has_alerts = observacao.has_alerts
        model.alertas_json = observacao.alerts
        model.metadata_json = observacao.metadata
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, observacao_id: UUID) -> ObservacaoMeteorologica | None:
        model = await self.session.get(ObservacaoMeteorologicaModel, observacao_id)
        return self._to_domain(model) if model else None

    async def list_by_estacao(
        self,
        estacao_id: UUID,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        limit: int = 100,
    ) -> list[ObservacaoMeteorologica]:
        stmt = select(ObservacaoMeteorologicaModel).where(
            ObservacaoMeteorologicaModel.estacao_id == estacao_id
        )
        if start_date is not None:
            stmt = stmt.where(ObservacaoMeteorologicaModel.data_observacao >= start_date)
        if end_date is not None:
            stmt = stmt.where(ObservacaoMeteorologicaModel.data_observacao <= end_date)
        stmt = stmt.order_by(ObservacaoMeteorologicaModel.data_observacao.desc()).limit(limit)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def list_with_alerts(
        self, start_date: datetime | None = None, end_date: datetime | None = None, limit: int = 50
    ) -> list[ObservacaoMeteorologica]:
        stmt = select(ObservacaoMeteorologicaModel).where(
            ObservacaoMeteorologicaModel.has_alerts.is_(True)
        )
        if start_date is not None:
            stmt = stmt.where(ObservacaoMeteorologicaModel.data_observacao >= start_date)
        if end_date is not None:
            stmt = stmt.where(ObservacaoMeteorologicaModel.data_observacao <= end_date)
        stmt = stmt.order_by(ObservacaoMeteorologicaModel.data_observacao.desc()).limit(limit)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def get_latest_by_estacao(self, estacao_id: UUID) -> ObservacaoMeteorologica | None:
        stmt = (
            select(ObservacaoMeteorologicaModel)
            .where(ObservacaoMeteorologicaModel.estacao_id == estacao_id)
            .order_by(ObservacaoMeteorologicaModel.data_observacao.desc())
            .limit(1)
        )
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    @staticmethod
    def _to_domain(model: ObservacaoMeteorologicaModel) -> ObservacaoMeteorologica:
        try:
            tipo = ObservationType(model.tipo)
        except ValueError:
            tipo = ObservationType.SURFACE
        observacao = ObservacaoMeteorologica(
            observacao_id=model.id,
            estacao_id=model.estacao_id,
            data_observacao=model.data_observacao,
            temperatura=model.temperatura,
            humidade=model.humidade,
            pressao=model.pressao,
            velocidade_vento=model.velocidade_vento,
            direcao_vento=model.direcao_vento,
            precipitacao=model.precipitacao,
            radiacao_solar=model.radiacao_solar,
            tipo=tipo,
            qualidade_dados=model.qualidade_dados,
            metadata=model.metadata_json,
            created_at=model.created_at,
        )
        observacao._alertas = list(model.alertas_json or [])
        return observacao
