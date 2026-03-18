from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from ....trade.external.domain.enums import StatusHabilitacao
from ....trade.external.domain.models import Importador

class ImportadorRepositoryPort(ABC):

    @abstractmethod
    async def save(self, importador: Importador) -> Importador:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Importador | None:
        pass

    @abstractmethod
    async def get_by_cnpj_cpf(self, cnpj_cpf: str) -> Importador | None:
        pass

    @abstractmethod
    async def list(self, *, status: StatusHabilitacao | None=None, municipio: str | None=None) -> list[Importador]:
        pass