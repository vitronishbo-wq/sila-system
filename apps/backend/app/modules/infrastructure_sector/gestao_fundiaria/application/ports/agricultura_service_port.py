from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class AgriculturaServicePort(ABC):
    @abstractmethod
    async def validar_produtor(self, produtor_id: UUID) -> bool:
        pass
