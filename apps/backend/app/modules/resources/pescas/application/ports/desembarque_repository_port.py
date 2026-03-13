from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.resources.pescas.domain.models.desembarque import Desembarque

class DesembarqueRepositoryPort(ABC):

    @abstractmethod
    async def save(self, desembarque: Desembarque) -> Desembarque:
        pass

    @abstractmethod
    async def get_by_id(self, desembarque_id: UUID) -> Desembarque | None:
        pass

    @abstractmethod
    async def list_by_captura(self, captura_id: UUID) -> list[Desembarque]:
        pass

    @abstractmethod
    async def list_by_porto(self, porto: str) -> list[Desembarque]:
        pass