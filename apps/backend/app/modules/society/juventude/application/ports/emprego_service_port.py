from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class EmpregoServicePort(ABC):
    @abstractmethod
    async def has_candidatura_ativa(self, citizen_id: UUID) -> bool:
        raise NotImplementedError
