from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from uuid import UUID, uuid4
from apps.backend.app.modules.governance.workflow.domain.enums import TaskStatus, TaskPriority

@dataclass
class WorkflowTask:
    """Tarefa a ser executada"""
    instance_id: UUID
    state_id: UUID
    transition_id: UUID
    title: str
    id: UUID = field(default_factory=uuid4)
    description: Optional[str] = None
    assigned_to: Optional[UUID] = None
    assigned_role: Optional[str] = None
    assignment_type: str = 'ROLE'
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    form_data: Dict[str, Any] = field(default_factory=dict)
    result_data: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    due_at: Optional[datetime] = None
    timeout_hours: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    updated_at: Optional[datetime] = None

    @property
    def is_pending(self) -> bool:
        return self.status == TaskStatus.PENDING

    @property
    def is_assigned(self) -> bool:
        return self.status == TaskStatus.ASSIGNED

    @property
    def is_completed(self) -> bool:
        return self.status == TaskStatus.COMPLETED

    @property
    def is_overdue(self) -> bool:
        """Verifica se está atrasado"""
        if not self.due_at:
            return False
        return datetime.now() > self.due_at

    @property
    def time_to_complete(self) -> Optional[timedelta]:
        """Tempo restante para conclusão"""
        if not self.due_at:
            return None
        return self.due_at - datetime.now() if self.due_at > datetime.now() else timedelta(0)

    def assign(self, user_id: UUID):
        """Atribui tarefa a um usuário"""
        self.assigned_to = user_id
        self.status = TaskStatus.ASSIGNED
        self.updated_at = datetime.now()

    def start(self):
        """Inicia a tarefa"""
        self.status = TaskStatus.IN_PROGRESS
        self.started_at = datetime.now()
        self.updated_at = datetime.now()

    def complete(self, result: Dict[str, Any]=None):
        """Completa a tarefa"""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()
        if result:
            self.result_data = result

    def skip(self, reason: str=None):
        """Pula a tarefa"""
        self.status = TaskStatus.SKIPPED
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()
        if reason:
            self.metadata['skip_reason'] = reason

    def cancel(self, reason: str=None):
        """Cancela a tarefa"""
        self.status = TaskStatus.CANCELLED
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()
        if reason:
            self.metadata['cancel_reason'] = reason

    def to_dict(self) -> dict:
        return {'id': str(self.id), 'instance_id': str(self.instance_id), 'state_id': str(self.state_id), 'transition_id': str(self.transition_id), 'title': self.title, 'description': self.description, 'assigned_to': str(self.assigned_to) if self.assigned_to else None, 'assigned_role': self.assigned_role, 'assignment_type': self.assignment_type, 'status': self.status.value, 'priority': self.priority.value, 'form_data': self.form_data, 'result_data': self.result_data, 'created_at': self.created_at.isoformat(), 'started_at': self.started_at.isoformat() if self.started_at else None, 'completed_at': self.completed_at.isoformat() if self.completed_at else None, 'due_at': self.due_at.isoformat() if self.due_at else None, 'is_overdue': self.is_overdue, 'time_to_complete_seconds': self.time_to_complete.total_seconds() if self.time_to_complete else None, 'metadata': self.metadata}