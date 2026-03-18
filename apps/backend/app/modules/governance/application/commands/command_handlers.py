"""Governance command handlers."""
import uuid
from apps.backend.app.modules.governance.application.commands.governance_commands import StartWorkflowCommand, TransitionWorkflowCommand, ApproveRequestCommand, RejectRequestCommand
from apps.backend.app.modules.governance.domain.models.workflow import Workflow
from apps.backend.app.modules.governance.domain.models.governance_request import GovernanceRequest
from apps.backend.app.modules.governance.domain.models.enums import WorkflowStatus
from apps.backend.app.modules.governance.domain.ports.aggregate_repository_port import AggregateRepositoryPort
from apps.backend.app.modules.governance.domain.ports.workflow_port import WorkflowPort

class StartWorkflowHandler:

    def __init__(self, workflow_repo: WorkflowPort):
        self.workflow_repo = workflow_repo

    async def handle(self, command: StartWorkflowCommand) -> Workflow:
        workflow = Workflow(id=str(uuid.uuid4()), process_name=command.process_name, owner_id=command.owner_id, total_steps=command.metadata.get('total_steps', 1) if command.metadata else 1, status=WorkflowStatus.DRAFT, metadata=command.metadata or {})
        saved = await self.workflow_repo.create(workflow)
        saved.start()
        await self.workflow_repo.save(saved)
        return saved

class TransitionWorkflowHandler:

    def __init__(self, workflow_repo: WorkflowPort):
        self.workflow_repo = workflow_repo

    async def handle(self, command: TransitionWorkflowCommand) -> Workflow:
        workflow = await self.workflow_repo.get_by_id(command.workflow_id)
        if not workflow:
            raise ValueError(f'Workflow {command.workflow_id} not found')
        workflow.transition(command.next_step)
        return await self.workflow_repo.save(workflow)

class ApproveRequestHandler:

    def __init__(self, repo: AggregateRepositoryPort):
        self.repo = repo

    async def handle(self, command: ApproveRequestCommand) -> GovernanceRequest:
        request = await self.repo.get_by_id(command.request_id)
        if not request:
            raise ValueError(f'Request {command.request_id} not found')
        request.approve(command.approver_id)
        return await self.repo.save(request)

class RejectRequestHandler:

    def __init__(self, repo: AggregateRepositoryPort):
        self.repo = repo

    async def handle(self, command: RejectRequestCommand) -> GovernanceRequest:
        request = await self.repo.get_by_id(command.request_id)
        if not request:
            raise ValueError(f'Request {command.request_id} not found')
        request.reject(command.approver_id, command.reason or '')
        return await self.repo.save(request)