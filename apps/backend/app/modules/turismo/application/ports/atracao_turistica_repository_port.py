from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.turismo.domain.enums import TipoAtracao
from app.modules.turismo.domain.models.atracao_turistica import AtracaoTuristica


class AtracaoTuristicaRepositoryPort(ABC):
    @abstractmethod
    async def save(self, atracao: AtracaoTuristica) -> AtracaoTuristica:
        pass

    @abstractmethod
    async def get_by_id(self, atracao_id: UUID) -> AtracaoTuristica | None:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo: str) -> AtracaoTuristica | None:
        pass

    @abstractmethod
    async def list(
        self,
        *,
        tipo: TipoAtracao | None = None,
        municipio: str | None = None,
        ativa: bool | None = None,
    ) -> list[AtracaoTuristica]:
        pass

    @abstractmethod
    async def delete(self, atracao_id: UUID) -> bool:
        pass

    @abstractmethod
    async def next_codigo(self, provincia: str) -> str:
        pass
