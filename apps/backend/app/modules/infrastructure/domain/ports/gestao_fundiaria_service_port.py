from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID

class GestaoFundiariaServicePort(ABC):

    @abstractmethod
    async def validar_imovel(self, imovel_id: UUID) -> bool:
        pass