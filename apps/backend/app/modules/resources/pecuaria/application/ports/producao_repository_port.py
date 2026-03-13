from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.resources.pecuaria.domain.models.producao_carne import ProducaoCarne
from app.modules.resources.pecuaria.domain.models.producao_leite import ProducaoLeite

class ProducaoRepositoryPort(ABC):

    @abstractmethod
    async def save_leite(self, item: ProducaoLeite) -> ProducaoLeite:
        pass

    @abstractmethod
    async def save_carne(self, item: ProducaoCarne) -> ProducaoCarne:
        pass

    @abstractmethod
    async def list_by_propriedade(self, propriedade_id: UUID) -> list[ProducaoLeite | ProducaoCarne]:
        pass