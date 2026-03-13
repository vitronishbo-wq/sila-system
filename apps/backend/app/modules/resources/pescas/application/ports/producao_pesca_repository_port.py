from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date
from app.modules.resources.pescas.domain.models.producao_pesca import ProducaoPesca

class ProducaoPescaRepositoryPort(ABC):

    @abstractmethod
    async def save(self, producao: ProducaoPesca) -> ProducaoPesca:
        pass

    @abstractmethod
    async def get_by_id(self, producao_id) -> ProducaoPesca | None:
        pass

    @abstractmethod
    async def list_by_periodo(self, data_inicio: date, data_fim: date) -> list[ProducaoPesca]:
        pass