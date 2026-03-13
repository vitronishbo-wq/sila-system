from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

class AssistenciaSocialServicePort(ABC):

    @abstractmethod
    async def get_beneficiario(self, citizen_id: UUID) -> dict[str, Any] | None:
        raise NotImplementedError

    @abstractmethod
    async def is_beneficiario_ativo(self, citizen_id: UUID) -> bool:
        raise NotImplementedError