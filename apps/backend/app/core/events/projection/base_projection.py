from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

class BaseProjection(ABC):

    @abstractmethod
    async def project(self, event: Any) -> None:
        raise NotImplementedError