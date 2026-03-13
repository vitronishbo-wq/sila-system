from __future__ import annotations
from abc import ABC, abstractmethod

class AgriculturaServicePort(ABC):

    @abstractmethod
    async def propriedade_existe(self, codigo_propriedade: str) -> bool:
        pass