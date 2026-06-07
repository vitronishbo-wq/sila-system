from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.educacao.domain.models import CicloEnsino, Escola, TipoEscola


class EscolaRepositoryPort(ABC):
    @abstractmethod
    async def save(self, escola: Escola) -> Escola:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Escola | None:
        pass

    @abstractmethod
    async def get_by_codigo_med(self, codigo_med: str) -> Escola | None:
        pass

    @abstractmethod
    async def list_by_filters(
        self,
        provincia: str | None = None,
        municipio: str | None = None,
        tipo: TipoEscola | None = None,
        ciclo: CicloEnsino | None = None,
        ativa: bool | None = None,
    ) -> list[Escola]:
        pass
