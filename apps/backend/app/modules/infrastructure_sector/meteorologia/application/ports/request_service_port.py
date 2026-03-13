from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

class RequestServicePort(ABC):

    @abstractmethod
    async def criar_request(self, request_data: dict[str, Any]) -> bool:
        raise NotImplementedError