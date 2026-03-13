from __future__ import annotations
from abc import ABC, abstractmethod

class IndustriaServicePort(ABC):

    @abstractmethod
    async def ping(self) -> bool:
        pass