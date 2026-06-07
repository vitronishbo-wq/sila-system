from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class IdentidadeAdapterPort(ABC):
    @abstractmethod
    async def validar_cidadao_ativo(self, citizen_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_cidadao(self, citizen_id: UUID) -> Any | None:
        raise NotImplementedError
