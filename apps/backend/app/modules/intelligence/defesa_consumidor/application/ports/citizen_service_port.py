from __future__ import annotations

from abc import ABC, abstractmethod


class CitizenServicePort(ABC):
    @abstractmethod
    async def exists(self, citizen_id: int) -> bool:
        pass
