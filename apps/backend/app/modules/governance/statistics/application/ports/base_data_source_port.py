from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime


class BaseDataSourcePort(ABC):
    @abstractmethod
    def get_metricas(self) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    def get_valor_metrica(
        self, metrica_nome: str, periodo_inicio: datetime, periodo_fim: datetime
    ) -> float:
        raise NotImplementedError

    @abstractmethod
    def get_timeseries(
        self, metrica_nome: str, periodo_inicio: datetime, periodo_fim: datetime
    ) -> list[dict]:
        raise NotImplementedError
