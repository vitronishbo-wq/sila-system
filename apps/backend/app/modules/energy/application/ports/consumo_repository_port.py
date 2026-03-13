from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.energy.domain.models import ConsumoEnergia

class ConsumoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: ConsumoEnergia) -> ConsumoEnergia:
        pass

    @abstractmethod
    async def get_by_id(self, consumo_id: UUID) -> ConsumoEnergia | None:
        pass

    @abstractmethod
    async def get_last_by_unidade(self, unidade_consumidora_id: UUID) -> ConsumoEnergia | None:
        pass

    @abstractmethod
    async def list(self, *, unidade_consumidora_id: UUID | None=None, cpf_titular: str | None=None) -> list[ConsumoEnergia]:
        pass
