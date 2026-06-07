from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class GeosampaServicePort(ABC):
    @abstractmethod
    async def validar_zona_pesca(self, zona_pesca_id: UUID) -> bool:
        pass
