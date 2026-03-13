from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

class GeosampaServicePort(ABC):

    @abstractmethod
    async def available(self) -> bool:
        pass

    @abstractmethod
    async def integration_payload(self) -> dict[str, Any]:
        pass