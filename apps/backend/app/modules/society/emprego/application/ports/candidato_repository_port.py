from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.society.emprego.domain.enums import Escolaridade, SituacaoProfissional
from apps.backend.app.modules.society.emprego.domain.models.candidato import Candidato


class CandidatoRepositoryPort(ABC):
    @abstractmethod
    async def save(self, candidato: Candidato) -> Candidato:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Candidato | None:
        pass

    @abstractmethod
    async def get_by_citizen(self, citizen_id: UUID) -> Candidato | None:
        pass

    @abstractmethod
    async def list_by_filtros(
        self,
        escolaridade: Escolaridade | None = None,
        situacao: SituacaoProfissional | None = None,
        area_interesse: str | None = None,
        ativos: bool = True,
    ) -> list[Candidato]:
        pass

    @abstractmethod
    async def next_numero_processo(self, ano: int) -> str:
        pass
