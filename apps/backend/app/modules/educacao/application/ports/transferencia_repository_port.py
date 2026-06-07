from __future__ import annotations

from abc import abstractmethod
from uuid import UUID

from apps.backend.app.modules.educacao.application.ports.workflow_repository_port import (
    WorkflowRepositoryPort,
)
from apps.backend.app.modules.educacao.domain.models._workflow_record import WorkflowRecord


class TransferenciaRepositoryPort(WorkflowRepositoryPort):
    @abstractmethod
    async def get_active_by_matricula(self, matricula_id: UUID) -> WorkflowRecord | None:
        raise NotImplementedError
