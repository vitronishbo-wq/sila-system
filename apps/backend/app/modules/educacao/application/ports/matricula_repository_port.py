from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from app.modules.educacao.domain.models import Matricula

class MatriculaRepositoryPort(ABC):
    """Porta para persistencia de matriculas."""

    @abstractmethod
    async def save(self, matricula: Matricula) -> Matricula:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[Matricula]:
        pass

    @abstractmethod
    async def get_by_citizen(self, citizen_id: UUID, ano_letivo_id: Optional[UUID]=None) -> list[Matricula]:
        pass

    @abstractmethod
    async def get_by_escola(self, escola_id: UUID, ano_letivo_id: UUID) -> list[Matricula]:
        pass

    @abstractmethod
    async def exists_active_for_citizen(self, citizen_id: UUID, ano_letivo_id: UUID) -> bool:
        pass

    @abstractmethod
    async def next_numero_processo(self, ano: int, escola_id: UUID) -> str:
        pass