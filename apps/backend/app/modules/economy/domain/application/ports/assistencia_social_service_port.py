from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

class AssistenciaSocialServicePort(ABC):

    @abstractmethod
    async def get_beneficio(self, beneficio_id: UUID) -> Any | None:
        pass

    @abstractmethod
    async def get_valor_beneficio(self, beneficio_id: UUID) -> float:
        pass

    @abstractmethod
    async def registrar_pagamento_beneficio(self, beneficio_id: UUID, pagamento_id: str, valor: float) -> None:
        pass