from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.society.juventude.domain.models._workflow_record import WorkflowRecord


class WorkflowRepositoryPort(ABC):
    @abstractmethod
    async def save(self, item: WorkflowRecord) -> WorkflowRecord:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, item_id: UUID) -> WorkflowRecord | None:
        raise NotImplementedError

    @abstractmethod
    async def list_by_citizen(
        self, citizen_id: UUID, service_type: str | None = None
    ) -> list[WorkflowRecord]:
        raise NotImplementedError

    @abstractmethod
    async def exists_active_for_citizen(self, citizen_id: UUID, service_type: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_numero_processo(self, ano: int, service_type: str, process_prefix: str) -> str:
        raise NotImplementedError
