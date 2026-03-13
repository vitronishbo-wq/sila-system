from __future__ import annotations
from abc import ABC, abstractmethod
from app.modules.resources.ambiente.domain.enums import StatusEstudoAmbiental, TipoEstudoAmbiental
from app.modules.resources.ambiente.domain.models.estudo_impacto import EstudoImpacto

class EstudoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: EstudoImpacto) -> EstudoImpacto:
        pass

    @abstractmethod
    async def get_by_numero(self, numero_estudo: str) -> EstudoImpacto | None:
        pass

    @abstractmethod
    async def list(self, *, numero_licenca: str | None=None, tipo: TipoEstudoAmbiental | None=None, status: StatusEstudoAmbiental | None=None) -> list[EstudoImpacto]:
        pass

    @abstractmethod
    async def next_numero(self) -> str:
        pass