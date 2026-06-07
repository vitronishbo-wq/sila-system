from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from apps.backend.app.modules.resources.pescas.domain.models.captura import Captura


class CapturaRepositoryPort(ABC):
    @abstractmethod
    async def save(self, captura: Captura) -> Captura:
        pass

    @abstractmethod
    async def get_by_id(self, captura_id: UUID) -> Captura | None:
        pass

    @abstractmethod
    async def list_by_embarcacao(self, embarcacao_id: UUID) -> list[Captura]:
        pass

    @abstractmethod
    async def list_by_licenca(self, licenca_id: UUID) -> list[Captura]:
        pass

    @abstractmethod
    async def list_by_periodo(self, data_inicio: datetime, data_fim: datetime) -> list[Captura]:
        pass
