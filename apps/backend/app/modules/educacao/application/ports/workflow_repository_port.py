from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from app.modules.educacao.domain.models._workflow_record import WorkflowRecord

class WorkflowRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: WorkflowRecord) -> WorkflowRecord:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[WorkflowRecord]:
        pass

    @abstractmethod
    async def list_by_citizen(self, citizen_id: UUID, service_type: str | None=None) -> list[WorkflowRecord]:
        pass

    @abstractmethod
    async def exists_active_for_citizen(self, citizen_id: UUID, service_type: str) -> bool:
        pass

    @abstractmethod
    async def next_numero_processo(self, ano: int, service_type: str, process_prefix: str) -> str:
        pass