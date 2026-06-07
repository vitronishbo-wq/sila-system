from __future__ import annotations

from abc import ABC, abstractmethod

from apps.backend.app.modules.resources.agricultura.domain.enums import StatusAssistencia
from apps.backend.app.modules.resources.agricultura.domain.models.assistencia_tecnica import (
    AssistenciaTecnica,
)


class AssistenciaRepositoryPort(ABC):
    @abstractmethod
    async def save(self, item: AssistenciaTecnica) -> AssistenciaTecnica:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_assistencia: str) -> AssistenciaTecnica | None:
        pass

    @abstractmethod
    async def list(
        self, *, codigo_propriedade: str | None = None, status: StatusAssistencia | None = None
    ) -> list[AssistenciaTecnica]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass
