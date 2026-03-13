from __future__ import annotations
from abc import ABC, abstractmethod
from apps.backend.app.modules.resources.pescas.domain.enums import TipoPescador
from apps.backend.app.modules.resources.pescas.domain.models.pescador import Pescador

class PescadorRepositoryPort(ABC):

    @abstractmethod
    async def save(self, pescador: Pescador) -> Pescador:
        pass

    @abstractmethod
    async def get_by_id(self, pescador_id) -> Pescador | None:
        pass

    @abstractmethod
    async def get_by_numero_registro(self, numero_registro: str) -> Pescador | None:
        pass

    @abstractmethod
    async def list_by_tipo(self, tipo: TipoPescador | None=None) -> list[Pescador]:
        pass

    @abstractmethod
    async def next_registro(self) -> str:
        pass