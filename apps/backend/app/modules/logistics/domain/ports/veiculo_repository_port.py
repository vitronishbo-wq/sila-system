from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.logistics.domain.enums import StatusVeiculoOperacional, TipoVeiculo
from apps.backend.app.modules.logistics.domain.models import Veiculo


class VeiculoRepositoryPort(ABC):
    @abstractmethod
    async def save(self, item: Veiculo) -> Veiculo:
        pass

    @abstractmethod
    async def get_by_id(self, veiculo_id: UUID) -> Veiculo | None:
        pass

    @abstractmethod
    async def get_by_placa(self, placa: str) -> Veiculo | None:
        pass

    @abstractmethod
    async def list(
        self,
        *,
        status: StatusVeiculoOperacional | None = None,
        tipo: TipoVeiculo | None = None,
        operadora_id: UUID | None = None,
    ) -> list[Veiculo]:
        pass
