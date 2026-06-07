from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

from apps.backend.app.modules.resources.pescas.domain.models.comercializacao_pesca import (
    ComercializacaoPesca,
)


class ComercializacaoPescaRepositoryPort(ABC):
    @abstractmethod
    async def save(self, item: ComercializacaoPesca) -> ComercializacaoPesca:
        pass

    @abstractmethod
    async def get_by_id(self, item_id) -> ComercializacaoPesca | None:
        pass

    @abstractmethod
    async def list_by_periodo(
        self, data_inicio: date, data_fim: date
    ) -> list[ComercializacaoPesca]:
        pass
