from __future__ import annotations

from abc import ABC, abstractmethod


class ObrasPublicasServicePort(ABC):
    @abstractmethod
    async def validar_corredor(self, codigo_corredor: str) -> bool:
        pass
