from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


@dataclass
class ApprovalStep:
    order: int
    role: str
    actor_id: Optional[str] = None
    status: ApprovalStatus = ApprovalStatus.PENDING
    comment: Optional[str] = None
    decided_at: Optional[datetime] = None


class ApprovalChain:
    """Cadeia de aprovações institucionais.
    Exemplo: Escola → Município → Província
    """

    def __init__(self, steps: list[tuple[str, str]]) -> None:
        self.steps: list[ApprovalStep] = [
            ApprovalStep(order=i, role=role)
            for i, (role, _) in enumerate(steps)
        ]
        self.current_step: int = 0
        self.created_at: datetime = datetime.now(timezone.utc)
        self.concluded_at: Optional[datetime] = None

    def approve(self, actor_id: str, comment: Optional[str] = None) -> bool:
        if self.is_completed():
            return False
        step = self.steps[self.current_step]
        step.actor_id = actor_id
        step.status = ApprovalStatus.APPROVED
        step.comment = comment
        step.decided_at = datetime.now(timezone.utc)
        self.current_step += 1
        if self.current_step >= len(self.steps):
            self.concluded_at = datetime.now(timezone.utc)
        return True

    def reject(self, actor_id: str, comment: str) -> None:
        step = self.steps[self.current_step]
        step.actor_id = actor_id
        step.status = ApprovalStatus.REJECTED
        step.comment = comment
        step.decided_at = datetime.now(timezone.utc)
        self.concluded_at = datetime.now(timezone.utc)

    def is_completed(self) -> bool:
        return self.concluded_at is not None

    def is_approved(self) -> bool:
        return all(s.status == ApprovalStatus.APPROVED for s in self.steps)
