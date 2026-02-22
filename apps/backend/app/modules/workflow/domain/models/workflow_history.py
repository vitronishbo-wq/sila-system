from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID, uuid4


@dataclass
class WorkflowHistory:
    """Histórico do workflow (auditoria)"""
    # Required fields
    instance_id: UUID
    action: str
    action_type: str  # TRANSITION, ASSIGNMENT, COMMENT, SYSTEM

    # Optional / defaults
    id: UUID = field(default_factory=uuid4)
    # Transição
    from_state_id: Optional[UUID] = None
    to_state_id: Optional[UUID] = None
    transition_id: Optional[UUID] = None
    task_id: Optional[UUID] = None
    
    # Ator
    performed_by: Optional[UUID] = None
    performed_by_role: Optional[str] = None
    
    # Dados
    comment: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Timestamp
    created_at: datetime = field(default_factory=datetime.now)
    
    @classmethod
    def transition(cls, instance_id: UUID, from_state: UUID, to_state: UUID,
                   transition_id: UUID, performed_by: UUID, comment: str = None):
        """Cria histórico de transição"""
        return cls(
            instance_id=instance_id,
            from_state_id=from_state,
            to_state_id=to_state,
            transition_id=transition_id,
            action="STATUS_CHANGED",
            action_type="TRANSITION",
            performed_by=performed_by,
            comment=comment
        )
    
    @classmethod
    def assignment(cls, instance_id: UUID, task_id: UUID, assigned_to: UUID,
                   performed_by: UUID):
        """Cria histórico de atribuição"""
        return cls(
            instance_id=instance_id,
            task_id=task_id,
            action="TASK_ASSIGNED",
            action_type="ASSIGNMENT",
            performed_by=performed_by,
            data={"assigned_to": str(assigned_to)}
        )
    
    @classmethod
    def comment(cls, instance_id: UUID, performed_by: UUID, comment: str):
        """Cria histórico de comentário"""
        return cls(
            instance_id=instance_id,
            action="COMMENT_ADDED",
            action_type="COMMENT",
            performed_by=performed_by,
            comment=comment
        )
    
    @classmethod
    def system(cls, instance_id: UUID, action: str, data: Dict[str, Any] = None):
        """Cria histórico de ação do sistema"""
        return cls(
            instance_id=instance_id,
            action=action,
            action_type="SYSTEM",
            data=data or {}
        )
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "instance_id": str(self.instance_id),
            "from_state_id": str(self.from_state_id) if self.from_state_id else None,
            "to_state_id": str(self.to_state_id) if self.to_state_id else None,
            "transition_id": str(self.transition_id) if self.transition_id else None,
            "task_id": str(self.task_id) if self.task_id else None,
            "action": self.action,
            "action_type": self.action_type,
            "performed_by": str(self.performed_by) if self.performed_by else None,
            "performed_by_role": self.performed_by_role,
            "comment": self.comment,
            "data": self.data,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }
