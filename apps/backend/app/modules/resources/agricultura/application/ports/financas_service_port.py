from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID

class FinancasServicePort(ABC):

    @abstractmethod
    async def registrar_credito_rural(self, produtor_id: UUID, valor: float) -> bool:
        pass