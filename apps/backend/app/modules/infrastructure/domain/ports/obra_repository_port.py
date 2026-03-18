from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.infrastructure.domain.enums import StatusObra
from apps.backend.app.modules.infrastructure.domain.models.obra import Obra

class ObraRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: Obra) -> Obra:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_obra: str) -> Obra | None:
        pass

    @abstractmethod
    async def list(self, *, status: StatusObra | None=None, orgao_responsavel_id: UUID | None=None, municipio: str | None=None, provincia: str | None=None) -> list[Obra]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass