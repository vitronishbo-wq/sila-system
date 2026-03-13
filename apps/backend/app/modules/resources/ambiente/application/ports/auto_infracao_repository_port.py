from __future__ import annotations
from abc import ABC, abstractmethod
from app.modules.resources.ambiente.domain.enums import StatusAutoInfracao, TipoAutoInfracao
from app.modules.resources.ambiente.domain.models.auto_infracao import AutoInfracao

class AutoInfracaoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: AutoInfracao) -> AutoInfracao:
        pass

    @abstractmethod
    async def get_by_numero(self, numero_auto: str) -> AutoInfracao | None:
        pass

    @abstractmethod
    async def list(self, *, numero_fiscalizacao: str | None=None, tipo: TipoAutoInfracao | None=None, status: StatusAutoInfracao | None=None) -> list[AutoInfracao]:
        pass

    @abstractmethod
    async def next_numero(self) -> str:
        pass