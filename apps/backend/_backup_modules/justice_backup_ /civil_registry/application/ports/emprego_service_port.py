from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

class EmpregoServicePort(ABC):

    @abstractmethod
    async def get_candidatura(self, citizen_id: UUID) -> dict[str, Any] | None:
        raise NotImplementedError

    @abstractmethod
    async def has_candidatura_ativa(self, citizen_id: UUID) -> bool:
        raise NotImplementedError