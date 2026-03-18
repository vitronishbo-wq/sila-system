"""Compliance command handlers."""
import uuid
from apps.backend.app.modules.compliance.application.commands.compliance_commands import LogAuditCommand, LogComplianceEventCommand, CreateComplianceCheckCommand
from apps.backend.app.modules.compliance.domain.models.audit_log import AuditLog
from apps.backend.app.modules.compliance.domain.models.compliance_check import ComplianceCheck
from apps.backend.app.modules.compliance.domain.models.enums import AuditLevel, ComplianceStatus
from apps.backend.app.modules.compliance.domain.ports.aggregate_repository_port import AggregateRepositoryPort
from apps.backend.app.modules.compliance.domain.ports.audit_log_port import AuditLogPort

class LogAuditHandler:

    def __init__(self, audit_repo: AuditLogPort):
        self.audit_repo = audit_repo

    async def handle(self, command: LogAuditCommand) -> AuditLog:
        audit_log = AuditLog(id=str(uuid.uuid4()), action=command.action, actor=command.actor, entity_type=command.entity_type, entity_id=command.entity_id, level=AuditLevel(command.level) if isinstance(command.level, str) else command.level, message=command.message or '', metadata=command.metadata or {})
        return await self.audit_repo.create(audit_log)

class LogComplianceEventHandler:

    def __init__(self, audit_repo: AuditLogPort):
        self.audit_repo = audit_repo

    async def handle(self, command: LogComplianceEventCommand) -> AuditLog:
        audit_log = AuditLog(id=str(uuid.uuid4()), action='COMPLIANCE_EVENT', actor=command.actor, entity_type=command.entity_type, entity_id=command.entity_id, level=AuditLevel.WARNING, message=command.message or '', metadata=command.metadata or {})
        return await self.audit_repo.create(audit_log)

class CreateComplianceCheckHandler:

    def __init__(self, repo: AggregateRepositoryPort):
        self.repo = repo

    async def handle(self, command: CreateComplianceCheckCommand) -> ComplianceCheck:
        compliance_check = ComplianceCheck(id=str(uuid.uuid4()), rule_id=command.rule_id, entity_type=command.entity_type, entity_id=command.entity_id, status=ComplianceStatus.PENDING, metadata=command.metadata or {})
        return await self.repo.save(compliance_check)