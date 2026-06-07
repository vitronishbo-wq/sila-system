from __future__ import annotations

from abc import ABC, abstractmethod


class RequestServicePort(ABC):
    @abstractmethod
    async def create(self, payload: dict) -> str:
        pass
