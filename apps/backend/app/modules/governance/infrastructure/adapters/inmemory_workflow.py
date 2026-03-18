from typing import Any, Dict, List
import uuid
from datetime import datetime
from apps.backend.app.modules.governance.domain.ports.workflow_port import WorkflowPort

class InMemoryWorkflow(WorkflowPort):
    """Adapter: In-memory workflow engine for governance processes."""

    def __init__(self):
        self.workflows: Dict[str, Dict[str, Any]] = {}

    async def start_workflow(self, workflow_name: str, context: Dict[str, Any]) -> str:
        """Start a new workflow."""
        workflow_id = str(uuid.uuid4())
        self.workflows[workflow_id] = {'id': workflow_id, 'name': workflow_name, 'state': 'started', 'context': context, 'created_at': datetime.now().isoformat(), 'updated_at': datetime.now().isoformat()}
        return workflow_id

    async def get_workflow_state(self, workflow_id: str) -> Dict[str, Any]:
        """Get current workflow state."""
        return self.workflows.get(workflow_id, {})

    async def transition_workflow(self, workflow_id: str, action: str, data: Dict[str, Any]) -> bool:
        """Transition workflow state."""
        if workflow_id not in self.workflows:
            return False
        workflow = self.workflows[workflow_id]
        workflow['context'].update(data)
        workflow['state'] = action
        workflow['updated_at'] = datetime.now().isoformat()
        return True

    async def list_workflows(self, filter_by: Dict=None, limit: int=100, offset: int=0) -> List[Dict[str, Any]]:
        """List workflows."""
        workflows = list(self.workflows.values())
        if filter_by:
            workflows = [w for w in workflows if all((w.get(k) == v for k, v in filter_by.items()))]
        return workflows[offset:offset + limit]