from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class JusticaServicePort(ABC):
    @abstractmethod
    async def possui_recurso_ativo(self, processo_id: UUID) -> bool:
        pass
