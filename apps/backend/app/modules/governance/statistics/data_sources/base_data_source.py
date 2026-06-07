from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime


class BaseDataSource(ABC):
    def __init__(self, module_name: str) -> None:
        self.module_name = module_name

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

    def validate_connection(self) -> bool:
        try:
            self.get_metricas()
            return True
        except Exception:
            return False
