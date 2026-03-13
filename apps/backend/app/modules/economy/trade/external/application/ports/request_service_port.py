from __future__ import annotations
from abc import ABC, abstractmethod

class RequestServicePort(ABC):

    @abstractmethod
    async def create_request(self, payload: dict):
        pass