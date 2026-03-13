from __future__ import annotations
from abc import ABC, abstractmethod
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusParcelamento, TipoParcelamento
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.parcelamento import Parcelamento

class ParcelamentoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: Parcelamento) -> Parcelamento:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_parcelamento: str) -> Parcelamento | None:
        pass

    @abstractmethod
    async def list(self, *, status: StatusParcelamento | None=None, tipo: TipoParcelamento | None=None, provincia: str | None=None) -> list[Parcelamento]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass