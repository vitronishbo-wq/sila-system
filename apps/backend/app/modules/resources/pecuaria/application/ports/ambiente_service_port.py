from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID

class AmbienteServicePort(ABC):

    @abstractmethod
    async def possui_licenciamento_ativo(self, propriedade_id: UUID) -> bool:
        pass