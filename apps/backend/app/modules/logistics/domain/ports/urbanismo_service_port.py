from __future__ import annotations

from abc import ABC, abstractmethod


class UrbanismoServicePort(ABC):
    @abstractmethod
    async def validar_zoneamento_rota(self, origem: str, destino: str) -> bool:
        pass
