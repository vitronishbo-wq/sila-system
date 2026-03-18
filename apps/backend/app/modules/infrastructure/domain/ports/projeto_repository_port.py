from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.infrastructure.domain.enums import StatusProjeto, TipoProjeto
from apps.backend.app.modules.infrastructure.domain.models.projeto_obra import ProjetoObra

class ProjetoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: ProjetoObra) -> ProjetoObra:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_projeto: str) -> ProjetoObra | None:
        pass

    @abstractmethod
    async def list(self, *, status: StatusProjeto | None=None, tipo: TipoProjeto | None=None, orgao_responsavel_id: UUID | None=None, obra_id: UUID | None=None) -> list[ProjetoObra]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass