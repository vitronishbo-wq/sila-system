from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID

class EducacaoServicePort(ABC):

    @abstractmethod
    async def is_estudante_ativo(self, citizen_id: UUID) -> bool:
        raise NotImplementedError