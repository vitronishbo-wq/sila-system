from __future__ import annotations
from abc import ABC, abstractmethod
from decimal import Decimal

class GeosampaServicePort(ABC):

    @abstractmethod
    async def validar_coordenadas(self, latitude: Decimal, longitude: Decimal) -> bool:
        pass