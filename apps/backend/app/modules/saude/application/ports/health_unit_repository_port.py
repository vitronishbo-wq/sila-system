from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID

class HealthUnitRepositoryPort(ABC):

    @abstractmethod
    async def get_by_id(self, health_unit_id: UUID):
        pass