from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.governance.workflow.domain.enums import WorkflowStatus
from apps.backend.app.modules.governance.workflow.domain.models.workflow_definition import (
    WorkflowDefinition,
)
from apps.backend.app.modules.governance.workflow.domain.models.workflow_history import (
    WorkflowHistory,
)
from apps.backend.app.modules.governance.workflow.domain.models.workflow_instance import (
    WorkflowInstance,
)
from apps.backend.app.modules.governance.workflow.domain.models.workflow_state import WorkflowState
from apps.backend.app.modules.governance.workflow.domain.models.workflow_transition import (
    WorkflowTransition,
)


class WorkflowRepositoryPort(ABC):
    """Interface do repositório de workflows"""

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def save_definition(self, definition: WorkflowDefinition) -> WorkflowDefinition:
        pass

    @abstractmethod
    async def get_definition(self, definition_id: UUID) -> WorkflowDefinition | None:
        pass

    @abstractmethod
    async def get_definition_by_code(
        self, code: str, version: int = None
    ) -> WorkflowDefinition | None:
        pass

    @abstractmethod
    async def list_definitions(
        self, skip: int = 0, limit: int = 100
    ) -> tuple[list[WorkflowDefinition], int]:
        pass

    @abstractmethod
    async def save_state(self, state: WorkflowState) -> WorkflowState:
        pass

    @abstractmethod
    async def get_states(self, workflow_id: UUID) -> list[WorkflowState]:
        pass

    @abstractmethod
    async def get_initial_state(self, workflow_id: UUID) -> WorkflowState | None:
        pass

    @abstractmethod
    async def get_state(self, state_id: UUID) -> WorkflowState | None:
        pass

    @abstractmethod
    async def save_transition(self, transition: WorkflowTransition) -> WorkflowTransition:
        pass

    @abstractmethod
    async def get_transitions(self, from_state_id: UUID) -> list[WorkflowTransition]:
        pass

    @abstractmethod
    async def get_transition(self, transition_id: UUID) -> WorkflowTransition | None:
        pass

    @abstractmethod
    async def get_transition_by_code(
        self, workflow_id: UUID, code: str
    ) -> WorkflowTransition | None:
        pass

    @abstractmethod
    async def save_instance(self, instance: WorkflowInstance) -> WorkflowInstance:
        pass

    @abstractmethod
    async def get_instance(self, instance_id: UUID) -> WorkflowInstance | None:
        pass

    @abstractmethod
    async def get_instance_by_entity(
        self, entity_type: str, entity_id: UUID
    ) -> WorkflowInstance | None:
        pass

    @abstractmethod
    async def list_instances(
        self,
        citizen_id: UUID = None,
        status: WorkflowStatus = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[WorkflowInstance], int]:
        pass

    @abstractmethod
    async def update_instance_state(self, instance_id: UUID, state_id: UUID) -> WorkflowInstance:
        pass

    @abstractmethod
    async def save_history(self, history: WorkflowHistory) -> WorkflowHistory:
        pass

    @abstractmethod
    async def get_instance_history(
        self, instance_id: UUID, limit: int = 100
    ) -> list[WorkflowHistory]:
        pass
