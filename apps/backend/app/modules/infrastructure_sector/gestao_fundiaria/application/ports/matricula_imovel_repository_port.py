from __future__ import annotations

from abc import ABC, abstractmethod

from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import (
    StatusMatriculaImovel,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.models.matricula_imovel import (
    MatriculaImovel,
)


class MatriculaImovelRepositoryPort(ABC):
    @abstractmethod
    async def save(self, item: MatriculaImovel) -> MatriculaImovel:
        pass

    @abstractmethod
    async def get_by_numero(self, numero_matricula: str) -> MatriculaImovel | None:
        pass

    @abstractmethod
    async def list(
        self,
        *,
        imovel_inscricao: str | None = None,
        status: StatusMatriculaImovel | None = None,
        ativo: bool | None = None,
    ) -> list[MatriculaImovel]:
        pass

    @abstractmethod
    async def next_numero(self) -> str:
        pass
