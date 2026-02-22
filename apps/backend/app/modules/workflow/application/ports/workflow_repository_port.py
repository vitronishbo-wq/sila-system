from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from uuid import UUID

from app.modules.workflow.domain.models.workflow_definition import WorkflowDefinition
from app.modules.workflow.domain.models.workflow_state import WorkflowState
from app.modules.workflow.domain.models.workflow_transition import WorkflowTransition
from app.modules.workflow.domain.models.workflow_instance import WorkflowInstance
from app.modules.workflow.domain.models.workflow_history import WorkflowHistory
from app.modules.workflow.domain.enums import WorkflowStatus


class WorkflowRepositoryPort(ABC):
    """Interface do repositório de workflows"""
    
    # Definitions
    @abstractmethod
    def save_definition(self, definition: WorkflowDefinition) -> WorkflowDefinition:
        pass
    
    @abstractmethod
    def get_definition(self, definition_id: UUID) -> Optional[WorkflowDefinition]:
        pass
    
    @abstractmethod
    def get_definition_by_code(self, code: str, version: int = None) -> Optional[WorkflowDefinition]:
        pass
    
    @abstractmethod
    def list_definitions(self, skip: int = 0, limit: int = 100) -> Tuple[List[WorkflowDefinition], int]:
        pass
    
    # States
    @abstractmethod
    def save_state(self, state: WorkflowState) -> WorkflowState:
        pass
    
    @abstractmethod
    def get_states(self, workflow_id: UUID) -> List[WorkflowState]:
        pass
    
    @abstractmethod
    def get_initial_state(self, workflow_id: UUID) -> Optional[WorkflowState]:
        pass
    
    # Transitions
    @abstractmethod
    def save_transition(self, transition: WorkflowTransition) -> WorkflowTransition:
        pass
    
    @abstractmethod
    def get_transitions(self, from_state_id: UUID) -> List[WorkflowTransition]:
        pass
    
    @abstractmethod
    def get_transition_by_code(self, workflow_id: UUID, code: str) -> Optional[WorkflowTransition]:
        pass
    
    # Instances
    @abstractmethod
    def save_instance(self, instance: WorkflowInstance) -> WorkflowInstance:
        pass
    
    @abstractmethod
    def get_instance(self, instance_id: UUID) -> Optional[WorkflowInstance]:
        pass
    
    @abstractmethod
    def get_instance_by_entity(self, entity_type: str, entity_id: UUID) -> Optional[WorkflowInstance]:
        pass
    
    @abstractmethod
    def list_instances(self, citizen_id: UUID = None, status: WorkflowStatus = None,
                       skip: int = 0, limit: int = 100) -> Tuple[List[WorkflowInstance], int]:
        pass
    
    @abstractmethod
    def update_instance_state(self, instance_id: UUID, state_id: UUID) -> WorkflowInstance:
        pass
    
    # History
    @abstractmethod
    def save_history(self, history: WorkflowHistory) -> WorkflowHistory:
        pass
    
    @abstractmethod
    def get_instance_history(self, instance_id: UUID, limit: int = 100) -> List[WorkflowHistory]:
        pass
