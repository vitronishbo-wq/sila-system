from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class CitizenServicePort(ABC):
    @abstractmethod
    async def exists(self, citizen_id: UUID) -> bool:
        pass
