from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from uuid import UUID

from app.modules.workflow.domain.models.workflow_task import WorkflowTask
from app.modules.workflow.domain.enums import TaskStatus


class TaskRepositoryPort(ABC):
    """Interface do repositório de tarefas"""
    
    @abstractmethod
    def save_task(self, task: WorkflowTask) -> WorkflowTask:
        pass
    
    @abstractmethod
    def get_task(self, task_id: UUID) -> Optional[WorkflowTask]:
        pass
    
    @abstractmethod
    def get_tasks_by_instance(self, instance_id: UUID) -> List[WorkflowTask]:
        pass
    
    @abstractmethod
    def get_pending_tasks(self, user_id: UUID = None, role: str = None,
                          skip: int = 0, limit: int = 100) -> Tuple[List[WorkflowTask], int]:
        pass
    
    @abstractmethod
    def get_assigned_tasks(self, user_id: UUID, status: TaskStatus = None,
                           skip: int = 0, limit: int = 100) -> Tuple[List[WorkflowTask], int]:
        pass
    
    @abstractmethod
    def get_tasks_by_status(self, status: TaskStatus, skip: int = 0, limit: int = 100) -> List[WorkflowTask]:
        pass
    
    @abstractmethod
    def get_overdue_tasks(self) -> List[WorkflowTask]:
        pass
    
    @abstractmethod
    def assign_task(self, task_id: UUID, user_id: UUID) -> WorkflowTask:
        pass
    
    @abstractmethod
    def complete_task(self, task_id: UUID, result: dict = None) -> WorkflowTask:
        pass
