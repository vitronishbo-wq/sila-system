from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class EducacaoAdapterPort(ABC):
    @abstractmethod
    async def has_matricula_ativa(self, citizen_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def validar_disponibilidade_vaga(self, *, turma_id: UUID, ano_letivo_id: UUID) -> bool:
        raise NotImplementedError
