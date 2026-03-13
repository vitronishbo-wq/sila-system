from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from app.modules.governance.workflow.domain.enums import TransitionType, AssignmentType

@dataclass
class WorkflowTransition:
    """Transição entre estados"""
    workflow_id: UUID
    from_state_id: UUID
    to_state_id: UUID
    code: str
    name: str
    id: UUID = field(default_factory=uuid4)
    description: Optional[str] = None
    transition_type: TransitionType = TransitionType.USER
    assignment_type: AssignmentType = AssignmentType.ROLE
    assignment_value: Optional[str] = None
    condition_expression: Optional[str] = None
    required_permissions: List[str] = field(default_factory=list)
    required_roles: List[str] = field(default_factory=list)
    pre_actions: Dict[str, Any] = field(default_factory=dict)
    post_actions: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.code or len(self.code.strip()) < 2:
            raise ValueError('Código deve ter pelo menos 2 caracteres')
        self.code = self.code.upper().strip()

    def can_execute(self, user_permissions: List[str], user_roles: List[str]) -> bool:
        """Verifica se usuário pode executar a transição"""
        if self.required_permissions:
            if not any((p in user_permissions for p in self.required_permissions)):
                return False
        if self.required_roles:
            if not any((r in user_roles for r in self.required_roles)):
                return False
        return True

    def to_dict(self) -> dict:
        return {'id': str(self.id), 'workflow_id': str(self.workflow_id), 'from_state_id': str(self.from_state_id), 'to_state_id': str(self.to_state_id), 'code': self.code, 'name': self.name, 'description': self.description, 'transition_type': self.transition_type.value, 'assignment_type': self.assignment_type.value, 'assignment_value': self.assignment_value, 'condition_expression': self.condition_expression, 'required_permissions': self.required_permissions, 'required_roles': self.required_roles, 'pre_actions': self.pre_actions, 'post_actions': self.post_actions, 'metadata': self.metadata, 'created_at': self.created_at.isoformat(), 'updated_at': self.updated_at.isoformat() if self.updated_at else None}