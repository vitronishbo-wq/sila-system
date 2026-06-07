from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class TaskResponse(BaseModel):
    """Response de tarefa"""

    id: UUID
    instance_id: UUID
    title: str
    description: str | None
    assigned_to: UUID | None
    assigned_role: str | None
    status: str
    priority: str
    form_data: dict[str, Any]
    created_at: datetime
    due_at: datetime | None
    is_overdue: bool


class TaskAssignRequest(BaseModel):
    """Request para atribuir tarefa"""

    user_id: UUID = Field(..., description="ID do usuário")


class TaskCompleteRequest(BaseModel):
    """Request para completar tarefa"""

    result: dict[str, Any] = Field(default_factory=dict)
    comment: str | None = None


class TaskListResponse(BaseModel):
    """Response para listagem de tarefas"""

    total: int
    items: list[TaskResponse]
