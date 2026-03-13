from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from apps.backend.app.modules.society.seguranca_social.domain.enums import StatusPensao, TipoPensao
from apps.backend.app.modules.society.seguranca_social.domain.models.pensao import Pensao

class PensaoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, pensao: Pensao) -> Pensao:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[Pensao]:
        pass

    @abstractmethod
    async def get_by_numero(self, numero_processo: str) -> Optional[Pensao]:
        pass

    @abstractmethod
    async def list_by_filtros(self, *, beneficiario_id: Optional[UUID]=None, tipo: Optional[TipoPensao]=None, status: Optional[StatusPensao]=None) -> list[Pensao]:
        pass

    @abstractmethod
    async def next_numero_processo(self, ano: int) -> str:
        pass