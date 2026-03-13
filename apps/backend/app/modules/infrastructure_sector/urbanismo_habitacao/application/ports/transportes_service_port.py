from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID

class TransportesServicePort(ABC):

    @abstractmethod
    async def validar_impacto_viario(self, *, zoneamento_id: UUID, quantidade_lotes: int) -> bool:
        pass