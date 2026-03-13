from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

class EducacaoServicePort(ABC):

    @abstractmethod
    async def get_matriculas_ativas(self, citizen_id: UUID) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    async def has_matricula_ativa(self, citizen_id: UUID) -> bool:
        raise NotImplementedError