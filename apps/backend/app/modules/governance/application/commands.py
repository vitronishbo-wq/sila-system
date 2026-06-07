"""
Governance Module Command Handlers
Shows the pattern for governance operations with event publishing.
"""

import logging
from datetime import UTC, date, datetime
from uuid import UUID

from apps.backend.app.core.events.event_bus import EventBus
from apps.backend.app.modules.governance.domain.events import (
    GovernmentDecisionMade,
    PolicyPublished,
    PublicServiceApproved,
)

logger = logging.getLogger(__name__)


class MakeGovernmentDecisionCommandHandler:
    """Make government decision."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        decision_id: UUID,
        decision_title: str,
        decision_type: str,
        decision_maker: str = "",
        affected_area: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Making government decision: {decision_title}")
        try:
            event = GovernmentDecisionMade(
                aggregate_id=decision_id,
                aggregate_type="GovernmentDecision",
                event_type="GovernmentDecisionMade",
                decision_id=decision_id,
                decision_title=decision_title,
                decision_date=date.today(),
                decision_type=decision_type,
                decision_maker=decision_maker,
                affected_area=affected_area,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "MakeGovernmentDecision",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Government decision made: {decision_id}")
        except Exception as e:
            logger.error(f"Error making government decision: {e}")
            raise


class PublishPolicyCommandHandler:
    """Publish government policy (ACAO compliance)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        policy_id: UUID,
        policy_number: str,
        policy_name: str,
        effective_date: date,
        published_by: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Publishing policy {policy_number}: {policy_name}")
        try:
            event = PolicyPublished(
                aggregate_id=policy_id,
                aggregate_type="GovernmentPolicy",
                event_type="PolicyPublished",
                policy_id=policy_id,
                policy_number=policy_number,
                policy_name=policy_name,
                publication_date=date.today(),
                effective_date=effective_date,
                published_by=published_by,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "PublishPolicy",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Policy published: {policy_number}")
        except Exception as e:
            logger.error(f"Error publishing policy: {e}")
            raise


class ApprovePublicServiceCommandHandler:
    """Approve public service (ACAO compliance)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        service_id: UUID,
        service_name: str,
        service_type: str = "",
        approval_authority: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Approving public service: {service_name}")
        try:
            event = PublicServiceApproved(
                aggregate_id=service_id,
                aggregate_type="PublicService",
                event_type="PublicServiceApproved",
                service_id=service_id,
                service_name=service_name,
                approval_date=date.today(),
                approval_authority=approval_authority,
                service_type=service_type,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "ApprovePublicService",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Public service approved: {service_id}")
        except Exception as e:
            logger.error(f"Error approving public service: {e}")
            raise
