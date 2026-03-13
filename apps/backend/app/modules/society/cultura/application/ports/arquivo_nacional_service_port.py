from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID

class ArquivoNacionalServicePort(ABC):

    @abstractmethod
    async def documento_exists(self, documento_id: UUID) -> bool:
        pass