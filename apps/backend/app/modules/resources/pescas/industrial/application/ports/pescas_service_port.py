from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class PescasServicePort(ABC):
    @abstractmethod
    async def armador_exists(self, armador_id: UUID) -> bool:
        pass
