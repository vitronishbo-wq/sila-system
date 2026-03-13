from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.domain.models.ocorrencia import Ocorrencia

class OcorrenciaRepositoryPort(ABC):

    @abstractmethod
    async def save(self, ocorrencia: Ocorrencia) -> Ocorrencia:
        ...

    @abstractmethod
    async def get_by_id(self, ocorrencia_id: UUID) -> Ocorrencia | None:
        ...

    @abstractmethod
    async def list_all(self) -> list[Ocorrencia]:
        ...

    @abstractmethod
    async def list_by_periodo(self, inicio: datetime, fim: datetime) -> list[Ocorrencia]:
        ...