from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID

class SaudeAdapterPort(ABC):

    @abstractmethod
    async def has_atendimento_ativo(self, citizen_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def count_atendimentos(self, citizen_id: UUID) -> int:
        raise NotImplementedError