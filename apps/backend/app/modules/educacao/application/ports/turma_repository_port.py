from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from app.modules.educacao.domain.models import Turma

class TurmaRepositoryPort(ABC):

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[Turma]:
        pass

    @abstractmethod
    async def count_matriculas_ativas(self, turma_id: UUID, ano_letivo_id: UUID) -> int:
        pass