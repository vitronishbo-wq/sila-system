from __future__ import annotations
from datetime import datetime
from apps.backend.app.modules.governance.statistics.application.ports.metrica_repository_port import MetricaRepositoryPort
from apps.backend.app.modules.governance.statistics.application.ports.timeseries_repository_port import TimeSeriesRepositoryPort
from apps.backend.app.modules.governance.statistics.domain.models.timeseries import TimeSeries
from apps.backend.app.modules.governance.statistics.exceptions import EstatisticaNotFoundError

class TimeSeriesService:

    def __init__(self, timeseries_repository: TimeSeriesRepositoryPort, metrica_repository: MetricaRepositoryPort) -> None:
        self.timeseries_repository = timeseries_repository
        self.metrica_repository = metrica_repository

    async def registrar_ponto(self, data: dict) -> TimeSeries:
        if not await self.metrica_repository.get_by_id(data['metrica_id']):
            raise EstatisticaNotFoundError('Metrica nao encontrada')
        point = TimeSeries(**data)
        return await self.timeseries_repository.create(point)

    async def listar_serie(self, metrica_id: int, inicio: datetime | None=None, fim: datetime | None=None, limit: int=200) -> list[TimeSeries]:
        if not await self.metrica_repository.get_by_id(metrica_id):
            raise EstatisticaNotFoundError('Metrica nao encontrada')
        return await self.timeseries_repository.list_by_metrica(metrica_id=metrica_id, inicio=inicio, fim=fim, limit=limit)

    async def obter_ultimo(self, metrica_id: int) -> TimeSeries | None:
        if not await self.metrica_repository.get_by_id(metrica_id):
            raise EstatisticaNotFoundError('Metrica nao encontrada')
        return await self.timeseries_repository.latest_by_metrica(metrica_id)