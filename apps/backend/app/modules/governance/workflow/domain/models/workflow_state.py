from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4


@dataclass
class WorkflowState:
    """Estado do workflow"""

    workflow_id: UUID
    code: str
    name: str
    id: UUID = field(default_factory=uuid4)
    description: str | None = None
    is_initial: bool = False
    is_final: bool = False
    is_auto_forward: bool = False
    timeout_hours: int | None = None
    form_schema: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime | None = None

    def __post_init__(self):
        if not self.code or len(self.code.strip()) < 2:
            raise ValueError("Código deve ter pelo menos 2 caracteres")
        self.code = self.code.upper().strip()

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "workflow_id": str(self.workflow_id),
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "is_initial": self.is_initial,
            "is_final": self.is_final,
            "is_auto_forward": self.is_auto_forward,
            "timeout_hours": self.timeout_hours,
            "form_schema": self.form_schema,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
