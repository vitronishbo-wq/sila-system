from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class GestaoFundiariaServicePort(ABC):
    @abstractmethod
    async def propriedade_existe(self, propriedade_id: UUID) -> bool:
        pass
