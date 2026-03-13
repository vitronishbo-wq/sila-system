from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class WorkflowServicePort(ABC):

    @abstractmethod
    async def abrir_fluxo(
        self,
        *,
        tipo_fluxo: str,
        entity_id: UUID,
        actor_id: UUID,
        health_unit_id: UUID,
        citizen_id: UUID,
        detalhes: dict,
    ) -> str | None:
        pass
