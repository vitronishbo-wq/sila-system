from __future__ import annotations
from abc import ABC, abstractmethod
from decimal import Decimal

class FinancasPublicasServicePort(ABC):

    @abstractmethod
    async def validar_capacidade_financiamento(self, valor: Decimal) -> bool:
        pass