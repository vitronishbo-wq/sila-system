from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class WorkflowServicePort(ABC):
    @abstractmethod
    async def iniciar_fluxo(self, *, entidade: str, referencia_id: UUID, contexto: dict) -> str:
        pass

    @abstractmethod
    async def registrar_evento(self, *, workflow_id: str, evento: str, payload: dict) -> None:
        pass
