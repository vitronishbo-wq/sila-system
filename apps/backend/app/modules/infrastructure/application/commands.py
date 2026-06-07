"""
Infrastructure Module Command Handlers
Shows the pattern for infrastructure management with event publishing.
"""

import logging
from datetime import UTC, date, datetime
from uuid import UUID

from apps.backend.app.core.events.event_bus import EventBus
from apps.backend.app.modules.infrastructure.domain.events import (
    InfrastructureAssetRegistered,
    MaintenancePlanApproved,
    MaintenanceWorkCompleted,
)

logger = logging.getLogger(__name__)


class RegisterInfrastructureAssetCommandHandler:
    """Register infrastructure asset."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        asset_id: UUID,
        asset_type: str,
        asset_name: str,
        location: str = "",
        registration_number: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Registering infrastructure asset {asset_name}")
        try:
            event = InfrastructureAssetRegistered(
                aggregate_id=asset_id,
                aggregate_type="InfrastructureAsset",
                event_type="InfrastructureAssetRegistered",
                asset_id=asset_id,
                asset_type=asset_type,
                asset_name=asset_name,
                location=location,
                registration_date=date.today(),
                registration_number=registration_number,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "RegisterInfrastructureAsset",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Infrastructure asset registered: {asset_id}")
        except Exception as e:
            logger.error(f"Error registering asset: {e}")
            raise


class ApproveMaintenancePlanCommandHandler:
    """Approve maintenance plan (ACAO compliance)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        plan_id: UUID,
        asset_id: UUID,
        approved_by: str = "",
        maintenance_scope: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Approving maintenance plan {plan_id}")
        try:
            event = MaintenancePlanApproved(
                aggregate_id=plan_id,
                aggregate_type="MaintenancePlan",
                event_type="MaintenancePlanApproved",
                plan_id=plan_id,
                asset_id=asset_id,
                approval_date=date.today(),
                approved_by=approved_by,
                maintenance_scope=maintenance_scope,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "ApproveMaintenancePlan",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Maintenance plan approved: {plan_id}")
        except Exception as e:
            logger.error(f"Error approving maintenance plan: {e}")
            raise


class CompleteMaintenanceWorkCommandHandler:
    """Complete maintenance work (ACAO compliance)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        work_id: UUID,
        asset_id: UUID,
        completed_by: str = "",
        work_quality_assessment: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Completing maintenance work {work_id}")
        try:
            event = MaintenanceWorkCompleted(
                aggregate_id=work_id,
                aggregate_type="MaintenanceWork",
                event_type="MaintenanceWorkCompleted",
                work_id=work_id,
                asset_id=asset_id,
                completion_date=date.today(),
                completed_by=completed_by,
                work_quality_assessment=work_quality_assessment,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "CompleteMaintenanceWork",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Maintenance work completed: {work_id}")
        except Exception as e:
            logger.error(f"Error completing maintenance work: {e}")
            raise
