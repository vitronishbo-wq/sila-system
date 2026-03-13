from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.resources.florestas.domain.models.plano_manejo_florestal import PlanoManejoFlorestal

class PlanoManejoFlorestalRepositoryPort(ABC):

    @abstractmethod
    async def save(self, plano: PlanoManejoFlorestal) -> PlanoManejoFlorestal:
        pass

    @abstractmethod
    async def get_by_id(self, plano_id: UUID) -> PlanoManejoFlorestal | None:
        pass

    @abstractmethod
    async def get_by_numero(self, numero_pmfs: str) -> PlanoManejoFlorestal | None:
        pass

    @abstractmethod
    async def list_by_unidade(self, unidade_manejo_id: UUID) -> list[PlanoManejoFlorestal]:
        pass