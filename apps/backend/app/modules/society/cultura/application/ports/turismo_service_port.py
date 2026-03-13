from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID

class TurismoServicePort(ABC):

    @abstractmethod
    async def atracao_exists(self, atracao_id: UUID) -> bool:
        pass