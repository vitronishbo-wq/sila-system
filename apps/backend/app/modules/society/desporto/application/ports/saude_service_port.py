from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class SaudeServicePort(ABC):
    @abstractmethod
    async def exame_exists(self, exame_id: UUID) -> bool:
        raise NotImplementedError
