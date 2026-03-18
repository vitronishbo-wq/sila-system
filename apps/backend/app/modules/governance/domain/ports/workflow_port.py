from abc import ABC, abstractmethod
from typing import Any, Dict, List

class WorkflowPort(ABC):
    """Port: Workflow management and state machine interface."""

    @abstractmethod
    async def start_workflow(self, workflow_name: str, context: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    async def get_workflow_state(self, workflow_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def transition_workflow(self, workflow_id: str, action: str, data: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    async def list_workflows(self, filter_by: Dict=None, limit: int=100, offset: int=0) -> List[Dict[str, Any]]:
        pass