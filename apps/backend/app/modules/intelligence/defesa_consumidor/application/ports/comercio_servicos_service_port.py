from __future__ import annotations
from abc import ABC, abstractmethod

class ComercioServicosServicePort(ABC):

    @abstractmethod
    async def estabelecimento_exists(self, estabelecimento_id: int) -> bool:
        pass