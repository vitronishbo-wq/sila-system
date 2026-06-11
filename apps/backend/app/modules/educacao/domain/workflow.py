
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID, uuid4
from datetime import datetime

class WorkflowStatus(StrEnum):
    PENDENTE = "pendente"
    APROVADO = "aprovado"
    REJEITADO = "rejeitado"

@dataclass
class WorkflowRecord:
    id: UUID = field(default_factory=uuid4)
    entity_id: UUID
    workflow_type: str
    status: WorkflowStatus = WorkflowStatus.PENDENTE
    territory_id: UUID
    created_by: UUID
    managed_by: UUID
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
