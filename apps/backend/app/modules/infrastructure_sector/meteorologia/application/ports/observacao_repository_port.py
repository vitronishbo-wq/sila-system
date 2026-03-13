from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.meteorologia.domain.models import ObservacaoMeteorologica

class ObservacaoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, observacao: ObservacaoMeteorologica) -> ObservacaoMeteorologica:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, observacao_id: UUID) -> ObservacaoMeteorologica | None:
        raise NotImplementedError

    @abstractmethod
    async def list_by_estacao(self, estacao_id: UUID, start_date: datetime | None=None, end_date: datetime | None=None, limit: int=100) -> list[ObservacaoMeteorologica]:
        raise NotImplementedError

    @abstractmethod
    async def list_with_alerts(self, start_date: datetime | None=None, end_date: datetime | None=None, limit: int=50) -> list[ObservacaoMeteorologica]:
        raise NotImplementedError

    @abstractmethod
    async def get_latest_by_estacao(self, estacao_id: UUID) -> ObservacaoMeteorologica | None:
        raise NotImplementedError