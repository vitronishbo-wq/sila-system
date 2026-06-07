from abc import ABC, abstractmethod
from typing import Any


class WorkflowPort(ABC):
    """Port: Workflow management and state machine interface."""

    @abstractmethod
    async def start_workflow(self, workflow_name: str, context: dict[str, Any]) -> str:
        pass

    @abstractmethod
    async def get_workflow_state(self, workflow_id: str) -> dict[str, Any]:
        pass

    @abstractmethod
    async def transition_workflow(
        self, workflow_id: str, action: str, data: dict[str, Any]
    ) -> bool:
        pass

    @abstractmethod
    async def list_workflows(
        self, filter_by: dict = None, limit: int = 100, offset: int = 0
    ) -> list[dict[str, Any]]:
        pass
