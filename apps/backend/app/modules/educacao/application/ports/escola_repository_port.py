from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from app.modules.educacao.domain.models import CicloEnsino, Escola, TipoEscola

class EscolaRepositoryPort(ABC):

    @abstractmethod
    async def save(self, escola: Escola) -> Escola:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[Escola]:
        pass

    @abstractmethod
    async def get_by_codigo_med(self, codigo_med: str) -> Optional[Escola]:
        pass

    @abstractmethod
    async def list_by_filters(self, provincia: Optional[str]=None, municipio: Optional[str]=None, tipo: Optional[TipoEscola]=None, ciclo: Optional[CicloEnsino]=None, ativa: Optional[bool]=None) -> list[Escola]:
        pass