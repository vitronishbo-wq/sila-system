from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.governance.workflow.domain.enums import TaskStatus
from apps.backend.app.modules.governance.workflow.domain.models.workflow_task import WorkflowTask


class TaskRepositoryPort(ABC):
    """Interface do repositório de tarefas"""

    @abstractmethod
    async def save_task(self, task: WorkflowTask) -> WorkflowTask:
        pass

    @abstractmethod
    async def get_task(self, task_id: UUID) -> WorkflowTask | None:
        pass

    @abstractmethod
    async def get_tasks_by_instance(self, instance_id: UUID) -> list[WorkflowTask]:
        pass

    @abstractmethod
    async def get_pending_tasks(
        self, user_id: UUID = None, role: str = None, skip: int = 0, limit: int = 100
    ) -> tuple[list[WorkflowTask], int]:
        pass

    @abstractmethod
    async def get_assigned_tasks(
        self, user_id: UUID, status: TaskStatus = None, skip: int = 0, limit: int = 100
    ) -> tuple[list[WorkflowTask], int]:
        pass

    @abstractmethod
    async def get_tasks_by_status(
        self, status: TaskStatus, skip: int = 0, limit: int = 100
    ) -> list[WorkflowTask]:
        pass

    @abstractmethod
    async def get_overdue_tasks(self) -> list[WorkflowTask]:
        pass

    @abstractmethod
    async def assign_task(self, task_id: UUID, user_id: UUID) -> WorkflowTask:
        pass

    @abstractmethod
    async def complete_task(self, task_id: UUID, result: dict = None) -> WorkflowTask:
        pass
