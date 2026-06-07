from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class JuventudeServicePort(ABC):
    @abstractmethod
    async def get_bolsa(self, referencia_id: UUID) -> Any | None:
        pass

    @abstractmethod
    async def get_valor_bolsa(self, referencia_id: UUID) -> float:
        pass

    @abstractmethod
    async def registrar_pagamento_bolsa(
        self, referencia_id: UUID, pagamento_id: str, valor: float
    ) -> None:
        pass
