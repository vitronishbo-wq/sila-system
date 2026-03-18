from __future__ import annotations
from abc import ABC, abstractmethod

class GeosampaServicePort(ABC):

    @abstractmethod
    async def rota_valida(self, itinerario: list[dict]) -> bool:
        pass