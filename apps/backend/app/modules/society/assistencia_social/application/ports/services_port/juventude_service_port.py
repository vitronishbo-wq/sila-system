from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class JuventudeServicePort(ABC):
    @abstractmethod
    async def is_jovem_em_risco(self, citizen_id: UUID) -> bool:
        raise NotImplementedError
