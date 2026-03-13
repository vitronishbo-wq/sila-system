from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID

class EducacaoServicePort(ABC):

    @abstractmethod
    async def instituicao_exists(self, instituicao_id: UUID) -> bool:
        pass