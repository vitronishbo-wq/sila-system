from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

class SaudeServicePort(ABC):

    @abstractmethod
    async def get_resumo_saude(self, citizen_id: UUID) -> dict[str, Any] | None:
        raise NotImplementedError

    @abstractmethod
    async def has_registro_medico(self, citizen_id: UUID) -> bool:
        raise NotImplementedError