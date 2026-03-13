from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID

class EducacaoServicePort(ABC):

    @abstractmethod
    async def has_matricula_ativa(self, citizen_id: UUID) -> bool:
        raise NotImplementedError