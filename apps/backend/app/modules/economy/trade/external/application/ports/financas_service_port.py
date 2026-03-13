from __future__ import annotations
from abc import ABC, abstractmethod

class FinancasServicePort(ABC):

    @abstractmethod
    async def ping(self) -> bool:
        pass