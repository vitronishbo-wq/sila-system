from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID

class ObrasPublicasServicePort(ABC):

    @abstractmethod
    async def validar_obra(self, obra_id: UUID) -> bool:
        pass