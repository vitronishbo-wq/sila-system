"""Compliance query handlers."""
from typing import List, Optional
from apps.backend.app.modules.compliance.application.queries.compliance_queries import GetAuditTrailQuery, ListComplianceEventsQuery, GetComplianceCheckQuery
from apps.backend.app.modules.compliance.domain.ports.aggregate_repository_port import AggregateRepositoryPort
from apps.backend.app.modules.compliance.domain.ports.audit_log_port import AuditLogPort

class GetAuditTrailHandler:

    def __init__(self, audit_repo: AuditLogPort):
        self.audit_repo = audit_repo

    async def handle(self, query: GetAuditTrailQuery) -> List:
        return await self.audit_repo.get_by_entity(query.entity_type, query.entity_id, limit=query.limit, offset=query.offset)

class ListComplianceEventsHandler:

    def __init__(self, audit_repo: AuditLogPort):
        self.audit_repo = audit_repo

    async def handle(self, query: ListComplianceEventsQuery) -> List:
        return await self.audit_repo.list_all(limit=query.limit, offset=query.offset)

class GetComplianceCheckHandler:

    def __init__(self, repo: AggregateRepositoryPort):
        self.repo = repo

    async def handle(self, query: GetComplianceCheckQuery):
        return await self.repo.get_by_id(query.check_id)