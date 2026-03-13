from __future__ import annotations
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.governance.statistics.application.ports.timeseries_repository_port import TimeSeriesRepositoryPort
from apps.backend.app.modules.governance.statistics.domain.models.timeseries import TimeSeries
from apps.backend.app.modules.governance.statistics.infrastructure.models.timeseries_model import TimeSeriesModel

class SQLAlchemyTimeSeriesRepository(TimeSeriesRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, point: TimeSeries) -> TimeSeries:
        model = TimeSeriesModel(metrica_id=point.metrica_id, timestamp=point.timestamp, valor=point.valor, dimensao_1=point.dimensao_1, dimensao_2=point.dimensao_2, dimensao_3=point.dimensao_3, origem=point.origem)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def list_by_metrica(self, metrica_id: int, inicio: datetime | None=None, fim: datetime | None=None, limit: int=200) -> list[TimeSeries]:
        stmt = select(TimeSeriesModel).where(TimeSeriesModel.metrica_id == metrica_id)
        if inicio is not None:
            stmt = stmt.where(TimeSeriesModel.timestamp >= inicio)
        if fim is not None:
            stmt = stmt.where(TimeSeriesModel.timestamp <= fim)
        stmt = stmt.order_by(TimeSeriesModel.timestamp.asc()).limit(limit)
        models = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(m) for m in models]

    async def latest_by_metrica(self, metrica_id: int) -> TimeSeries | None:
        stmt = select(TimeSeriesModel).where(TimeSeriesModel.metrica_id == metrica_id).order_by(TimeSeriesModel.timestamp.desc()).limit(1)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    @staticmethod
    def _to_domain(model: TimeSeriesModel) -> TimeSeries:
        return TimeSeries(id=model.id, metrica_id=model.metrica_id, timestamp=model.timestamp, valor=model.valor, dimensao_1=model.dimensao_1, dimensao_2=model.dimensao_2, dimensao_3=model.dimensao_3, origem=model.origem, criado_em=model.criado_em)