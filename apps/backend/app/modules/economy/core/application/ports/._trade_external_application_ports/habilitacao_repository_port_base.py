from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID
from ....trade.external.domain.enums import StatusHabilitacao
from ....trade.external.domain.models.habilitacao_base import HabilitacaoBase
THabilitacao = TypeVar('THabilitacao', bound=HabilitacaoBase)

class HabilitacaoRepositoryPortBase(ABC, Generic[THabilitacao]):

    @abstractmethod
    async def save(self, habilitacao: THabilitacao) -> THabilitacao:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> THabilitacao | None:
        pass

    @abstractmethod
    async def get_by_numero_processo(self, numero_processo: str) -> THabilitacao | None:
        pass

    @abstractmethod
    async def list(self, *, status: StatusHabilitacao | None=None) -> list[THabilitacao]:
        pass