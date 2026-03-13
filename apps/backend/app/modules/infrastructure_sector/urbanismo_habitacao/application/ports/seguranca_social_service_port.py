from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID

class SegurancaSocialServicePort(ABC):

    @abstractmethod
    async def validar_cadastro_social(self, citizen_id: UUID) -> bool:
        pass