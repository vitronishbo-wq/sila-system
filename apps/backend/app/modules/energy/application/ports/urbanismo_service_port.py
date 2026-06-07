from __future__ import annotations

from abc import ABC, abstractmethod


class UrbanismoServicePort(ABC):
    @abstractmethod
    async def validar_zoneamento_energia(self, municipio: str, provincia: str) -> bool:
        pass
