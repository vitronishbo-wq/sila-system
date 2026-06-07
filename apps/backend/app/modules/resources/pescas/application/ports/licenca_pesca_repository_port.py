from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID

from apps.backend.app.modules.resources.pescas.domain.models.licenca_pesca import LicencaPesca


class LicencaPescaRepositoryPort(ABC):
    @abstractmethod
    async def save(self, licenca: LicencaPesca) -> LicencaPesca:
        pass

    @abstractmethod
    async def get_by_id(self, licenca_id: UUID) -> LicencaPesca | None:
        pass

    @abstractmethod
    async def get_by_numero(self, numero_licenca: str) -> LicencaPesca | None:
        pass

    @abstractmethod
    async def list_by_embarcacao(self, embarcacao_id: UUID) -> list[LicencaPesca]:
        pass

    @abstractmethod
    async def list_validas(self, referencia: date) -> list[LicencaPesca]:
        pass

    @abstractmethod
    async def next_numero(self) -> str:
        pass
