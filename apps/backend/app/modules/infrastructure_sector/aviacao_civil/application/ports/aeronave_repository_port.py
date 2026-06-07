from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.infrastructure_sector.aviacao_civil.domain.models.aeronave import (
    Aeronave,
)


class AeronaveRepositoryPort(ABC):
    @abstractmethod
    async def save(self, aeronave: Aeronave) -> Aeronave: ...

    @abstractmethod
    async def get_by_id(self, aeronave_id: UUID) -> Aeronave | None: ...

    @abstractmethod
    async def get_by_matricula(self, matricula: str) -> Aeronave | None: ...

    @abstractmethod
    async def list_all(self) -> list[Aeronave]: ...
