from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class CitizenServicePort(ABC):
    @abstractmethod
    async def is_citizen_active(self, citizen_id: UUID) -> bool:
        raise NotImplementedError
