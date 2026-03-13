from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

class SaudeServicePort(ABC):

    @abstractmethod
    async def get_atendimento(self, atendimento_id: UUID) -> Any | None:
        pass

    @abstractmethod
    async def get_valor_servico(self, atendimento_id: UUID) -> float:
        pass

    @abstractmethod
    async def registrar_pagamento_servico(self, atendimento_id: UUID, pagamento_id: str, valor: float) -> None:
        pass