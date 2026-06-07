from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.educacao.domain.models import Turma


class TurmaRepositoryPort(ABC):
    @abstractmethod
    async def get_by_id(self, id: UUID, for_update: bool = False) -> Turma | None:
        pass

    @abstractmethod
    async def count_matriculas_ativas(self, turma_id: UUID, ano_letivo_id: UUID, for_update: bool = False) -> int:
        """Contar matrículas ativas COM opção de lock pessimista.
        
        CRÍTICO: PASSO 6 - Para evitar race condition no check de disponibilidade de vaga,
        use for_update=True dentro de uma transação explícita.
        """
        pass
