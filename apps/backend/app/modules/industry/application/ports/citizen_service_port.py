from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class CitizenServicePort(ABC):
    @abstractmethod
    async def get_by_id(self, citizen_id: UUID):
        pass
