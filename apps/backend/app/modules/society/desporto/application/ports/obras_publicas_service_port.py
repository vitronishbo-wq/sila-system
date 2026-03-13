from __future__ import annotations
from abc import ABC, abstractmethod

class ObrasPublicasServicePort(ABC):

    @abstractmethod
    async def obra_exists(self, codigo_obra: str) -> bool:
        raise NotImplementedError