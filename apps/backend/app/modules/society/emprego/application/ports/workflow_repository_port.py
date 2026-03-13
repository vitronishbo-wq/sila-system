from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from apps.backend.app.modules.society.emprego.domain.models._workflow_record import WorkflowEmpregoRecord

class WorkflowRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: WorkflowEmpregoRecord) -> WorkflowEmpregoRecord:
        pass

    @abstractmethod
    async def get_by_id(self, item_id: UUID) -> Optional[WorkflowEmpregoRecord]:
        pass

    @abstractmethod
    async def list_by_citizen(self, citizen_id: UUID, service_type: str | None=None) -> list[WorkflowEmpregoRecord]:
        pass

    @abstractmethod
    async def exists_active_for_citizen(self, citizen_id: UUID, service_type: str) -> bool:
        pass

    @abstractmethod
    async def next_numero_processo(self, ano: int, prefix: str) -> str:
        pass