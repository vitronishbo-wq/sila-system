from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID
from apps.backend.app.modules.logistics.domain.enums import StatusViagem
from apps.backend.app.modules.logistics.domain.models import Viagem

class ViagemRepositoryPort(ABC):

    @abstractmethod
    async def save(self, viagem: Viagem) -> Viagem:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Viagem | None:
        pass

    @abstractmethod
    async def list(self, *, status: StatusViagem | None=None, linha_id: UUID | None=None, veiculo_id: UUID | None=None) -> list[Viagem]:
        pass

    @abstractmethod
    async def has_active_for_veiculo(self, *, veiculo_id: UUID, inicio: datetime, fim: datetime, ignore_viagem_id: UUID | None=None) -> bool:
        pass
