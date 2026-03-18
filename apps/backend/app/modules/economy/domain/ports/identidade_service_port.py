from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

class IdentidadeServicePort(ABC):

    @abstractmethod
    async def get_cidadao(self, citizen_id: UUID) -> Any | None:
        pass

    @abstractmethod
    async def validar_cidadao_ativo(self, citizen_id: UUID) -> bool:
        pass