from __future__ import annotations

from abc import ABC, abstractmethod


class ComercioServicePort(ABC):
    @abstractmethod
    async def ping(self) -> bool:
        pass
