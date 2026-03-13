from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from apps.backend.app.modules.educacao.domain.enums import TipoInscricao
from apps.backend.app.modules.educacao.domain.models.inscricao_basica import InscricaoBasica
from apps.backend.app.modules.educacao.domain.models.inscricao_secundaria import InscricaoSecundaria
from apps.backend.app.modules.educacao.domain.models.inscricao_superior import InscricaoSuperior
from apps.backend.app.modules.educacao.domain.models.inscricao_tecnico import InscricaoTecnico
InscricaoEntity = InscricaoBasica | InscricaoSecundaria | InscricaoSuperior | InscricaoTecnico

class InscricaoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, inscricao: InscricaoEntity) -> InscricaoEntity:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[InscricaoEntity]:
        pass

    @abstractmethod
    async def get_by_citizen(self, citizen_id: UUID, tipo: TipoInscricao | None=None) -> list[InscricaoEntity]:
        pass

    @abstractmethod
    async def exists_active_for_citizen(self, citizen_id: UUID, tipo: TipoInscricao) -> bool:
        pass

    @abstractmethod
    async def next_numero_processo(self, ano: int, tipo: TipoInscricao) -> str:
        pass