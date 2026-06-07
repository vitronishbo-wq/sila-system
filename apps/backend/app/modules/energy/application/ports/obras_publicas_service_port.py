from __future__ import annotations

from abc import ABC, abstractmethod


class ObrasPublicasServicePort(ABC):
    @abstractmethod
    async def validar_obra_energia(self, obra_id: str) -> bool:
        pass
