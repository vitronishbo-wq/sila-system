from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class SaudeServicePort(ABC):
    @abstractmethod
    async def validar_laudo_pcd(self, *, citizen_id: UUID, laudo_id: UUID, cid: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def verificar_cobertura_idoso(self, *, citizen_id: UUID) -> bool:
        raise NotImplementedError
