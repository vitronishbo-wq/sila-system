from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class EmpregoServicePort(ABC):
    @abstractmethod
    async def get_contrato(self, contrato_id: UUID) -> Any | None:
        pass

    @abstractmethod
    async def get_valor_salario(self, contrato_id: UUID) -> float:
        pass

    @abstractmethod
    async def registrar_pagamento_salario(
        self, contrato_id: UUID, pagamento_id: str, valor: float
    ) -> None:
        pass
