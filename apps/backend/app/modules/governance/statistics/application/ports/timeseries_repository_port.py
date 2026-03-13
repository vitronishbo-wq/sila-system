from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from app.modules.governance.statistics.domain.models.timeseries import TimeSeries

class TimeSeriesRepositoryPort(ABC):

    @abstractmethod
    async def create(self, point: TimeSeries) -> TimeSeries:
        raise NotImplementedError

    @abstractmethod
    async def list_by_metrica(self, metrica_id: int, inicio: datetime | None=None, fim: datetime | None=None, limit: int=200) -> list[TimeSeries]:
        raise NotImplementedError

    @abstractmethod
    async def latest_by_metrica(self, metrica_id: int) -> TimeSeries | None:
        raise NotImplementedError