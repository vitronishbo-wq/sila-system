from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class QueryHandler(ABC):
    @abstractmethod
    async def handle(self, query: Any):
        raise NotImplementedError
