from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID

class RequestServicePort(ABC):

    @abstractmethod
    async def create_energy_request(self, *, entity_id: UUID, citizen_id: UUID, metadata: dict):
        pass