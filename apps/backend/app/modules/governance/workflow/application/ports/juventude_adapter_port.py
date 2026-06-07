from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class JuventudeAdapterPort(ABC):
    @abstractmethod
    async def has_jovem(self, citizen_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def is_jovem_em_risco(self, citizen_id: UUID) -> bool:
        raise NotImplementedError
