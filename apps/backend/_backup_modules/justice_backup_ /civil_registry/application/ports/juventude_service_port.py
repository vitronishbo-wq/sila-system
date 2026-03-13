from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

class JuventudeServicePort(ABC):

    @abstractmethod
    async def get_perfil_jovem(self, citizen_id: UUID) -> dict[str, Any] | None:
        raise NotImplementedError

    @abstractmethod
    async def is_jovem_em_risco(self, citizen_id: UUID) -> bool:
        raise NotImplementedError