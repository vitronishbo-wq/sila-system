"""Governance query handlers."""
from typing import List, Optional
from apps.backend.app.modules.governance.application.queries.governance_queries import GetWorkflowQuery, ListWorkflowsQuery, GetGovernanceRequestQuery, ListPendingApprovalsQuery
from apps.backend.app.modules.governance.domain.ports.aggregate_repository_port import AggregateRepositoryPort
from apps.backend.app.modules.governance.domain.ports.workflow_port import WorkflowPort

class GetWorkflowHandler:

    def __init__(self, workflow_repo: WorkflowPort):
        self.workflow_repo = workflow_repo

    async def handle(self, query: GetWorkflowQuery):
        return await self.workflow_repo.get_by_id(query.workflow_id)

class ListWorkflowsHandler:

    def __init__(self, workflow_repo: WorkflowPort):
        self.workflow_repo = workflow_repo

    async def handle(self, query: ListWorkflowsQuery) -> List:
        return await self.workflow_repo.list_by_owner(query.owner_id, limit=query.limit, offset=query.offset)

class GetGovernanceRequestHandler:

    def __init__(self, repo: AggregateRepositoryPort):
        self.repo = repo

    async def handle(self, query: GetGovernanceRequestQuery):
        return await self.repo.get_by_id(query.request_id)

class ListPendingApprovalsHandler:

    def __init__(self, repo: AggregateRepositoryPort):
        self.repo = repo

    async def handle(self, query: ListPendingApprovalsQuery) -> List:
        return await self.repo.list_pending(limit=query.limit, offset=query.offset)