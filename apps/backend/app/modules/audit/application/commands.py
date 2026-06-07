"""
Audit Module Command Handlers
Shows the pattern for audit operations with event publishing.
"""

import logging
from datetime import UTC, date, datetime
from uuid import UUID

from apps.backend.app.core.events.event_bus import EventBus
from apps.backend.app.modules.audit.domain.events import (
    AuditExecutionStarted,
    AuditFindingReported,
    AuditProgramCreated,
)

logger = logging.getLogger(__name__)


class CreateAuditProgramCommandHandler:
    """Create audit program."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        program_id: UUID,
        program_name: str,
        audit_type: str,
        start_date: date,
        end_date: date,
        auditee_id: UUID | None = None,
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Creating audit program: {program_name}")
        try:
            event = AuditProgramCreated(
                aggregate_id=program_id,
                aggregate_type="AuditProgram",
                event_type="AuditProgramCreated",
                program_id=program_id,
                program_name=program_name,
                audit_type=audit_type,
                start_date=start_date,
                end_date=end_date,
                auditee_id=auditee_id,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "CreateAuditProgram",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Audit program created: {program_id}")
        except Exception as e:
            logger.error(f"Error creating audit program: {e}")
            raise


class StartAuditExecutionCommandHandler:
    """Start audit execution."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        audit_id: UUID,
        program_id: UUID,
        audit_team: str = "",
        scope: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Starting audit execution {audit_id}")
        try:
            event = AuditExecutionStarted(
                aggregate_id=audit_id,
                aggregate_type="Audit",
                event_type="AuditExecutionStarted",
                audit_id=audit_id,
                program_id=program_id,
                execution_date=date.today(),
                audit_team=audit_team,
                scope=scope,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "StartAuditExecution",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Audit execution started: {audit_id}")
        except Exception as e:
            logger.error(f"Error starting audit execution: {e}")
            raise


class ReportAuditFindingCommandHandler:
    """Report audit finding (ACAO compliance)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        finding_id: UUID,
        audit_id: UUID,
        area_of_concern: str,
        severity: str = "medium",
        recommended_action: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Reporting audit finding: {area_of_concern}")
        try:
            event = AuditFindingReported(
                aggregate_id=finding_id,
                aggregate_type="AuditFinding",
                event_type="AuditFindingReported",
                finding_id=finding_id,
                audit_id=audit_id,
                area_of_concern=area_of_concern,
                finding_date=date.today(),
                severity=severity,
                recommended_action=recommended_action,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "ReportAuditFinding",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Audit finding reported: {finding_id}")
        except Exception as e:
            logger.error(f"Error reporting audit finding: {e}")
            raise
