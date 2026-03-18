from __future__ import annotations
from abc import ABC, abstractmethod
from decimal import Decimal
from uuid import UUID

class FinancasPublicasServicePort(ABC):

    @abstractmethod
    async def reservar_dotacao(self, orgao_id: UUID, valor: Decimal) -> bool:
        pass