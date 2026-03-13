from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.governance.cooperacao_internacional.domain.models.projeto_cooperacao import ProjetoCooperacao

class ProjetoCooperacaoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, projeto: ProjetoCooperacao) -> ProjetoCooperacao:
        ...

    @abstractmethod
    async def get_by_id(self, projeto_id: UUID) -> ProjetoCooperacao | None:
        ...

    @abstractmethod
    async def list_all(self) -> list[ProjetoCooperacao]:
        ...