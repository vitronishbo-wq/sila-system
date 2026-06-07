from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class MediacaoRepositoryPort(ABC):
    @abstractmethod
    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        pass
