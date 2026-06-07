from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.society.seguranca_social.domain.enums import StatusPensao, TipoPensao
from apps.backend.app.modules.society.seguranca_social.domain.models.pensao import Pensao


class PensaoRepositoryPort(ABC):
    @abstractmethod
    async def save(self, pensao: Pensao) -> Pensao:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Pensao | None:
        pass

    @abstractmethod
    async def get_by_numero(self, numero_processo: str) -> Pensao | None:
        pass

    @abstractmethod
    async def list_by_filtros(
        self,
        *,
        beneficiario_id: UUID | None = None,
        tipo: TipoPensao | None = None,
        status: StatusPensao | None = None,
    ) -> list[Pensao]:
        pass

    @abstractmethod
    async def next_numero_processo(self, ano: int) -> str:
        pass
