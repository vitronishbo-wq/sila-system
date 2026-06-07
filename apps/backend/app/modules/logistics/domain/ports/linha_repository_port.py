from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.logistics.domain.enums import ModalTransporte, StatusLinha
from apps.backend.app.modules.logistics.domain.models import Linha


class LinhaRepositoryPort(ABC):
    @abstractmethod
    async def save(self, item: Linha) -> Linha:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo: str) -> Linha | None:
        pass

    @abstractmethod
    async def get_by_id(self, linha_id: UUID) -> Linha | None:
        pass

    @abstractmethod
    async def list(
        self,
        *,
        status: StatusLinha | None = None,
        modal: ModalTransporte | None = None,
        operadora_id: UUID | None = None,
        origem: str | None = None,
        destino: str | None = None,
    ) -> list[Linha]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass
