from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class EducacaoServicePort(ABC):
    @abstractmethod
    async def get_matricula(self, matricula_id: UUID | str) -> Any | None:
        pass

    @abstractmethod
    async def get_valor_propina(self, matricula_id: UUID | str) -> float:
        pass

    @abstractmethod
    async def registrar_pagamento_propina(
        self, matricula_id: UUID | str, pagamento_id: str, valor: float
    ) -> None:
        pass
