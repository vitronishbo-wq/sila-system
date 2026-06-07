"""
Economy Module Command Handlers
Shows the pattern for economic operations with event publishing.
"""

import logging
from datetime import UTC, date, datetime
from uuid import UUID

from apps.backend.app.core.events.event_bus import EventBus
from apps.backend.app.modules.economy.domain.events import (
    EconomicActivityStarted,
    EconomicAgentRegistered,
    TaxRegistrationIssued,
)

logger = logging.getLogger(__name__)


class RegisterEconomicAgentCommandHandler:
    """Register an economic agent."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        agent_id: UUID,
        agent_name: str,
        agent_type: str,
        registration_number: str = "",
        sector: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Registering economic agent {agent_name}")
        try:
            event = EconomicAgentRegistered(
                aggregate_id=agent_id,
                aggregate_type="EconomicAgent",
                event_type="EconomicAgentRegistered",
                agent_id=agent_id,
                agent_name=agent_name,
                agent_type=agent_type,
                registration_number=registration_number,
                sector=sector,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "RegisterEconomicAgent",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Economic agent registered: {agent_id}")
        except Exception as e:
            logger.error(f"Error registering economic agent: {e}")
            raise


class StartEconomicActivityCommandHandler:
    """Start economic activity (ACAO compliance)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        activity_id: UUID,
        agent_id: UUID,
        activity_code: str,
        activity_description: str,
        registered_by: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Starting economic activity {activity_code}")
        try:
            event = EconomicActivityStarted(
                aggregate_id=activity_id,
                aggregate_type="EconomicActivity",
                event_type="EconomicActivityStarted",
                agent_id=agent_id,
                activity_code=activity_code,
                activity_description=activity_description,
                start_date=date.today(),
                registered_by=registered_by,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "agent_id": str(agent_id),
                    "command_name": "StartEconomicActivity",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Economic activity started: {activity_id}")
        except Exception as e:
            logger.error(f"Error starting economic activity: {e}")
            raise


class IssueTaxRegistrationCommandHandler:
    """Issue tax registration (ACAO compliance)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        tax_id: str,
        agent_id: UUID,
        tax_authority: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Issuing tax registration {tax_id}")
        try:
            event = TaxRegistrationIssued(
                aggregate_id=agent_id,
                aggregate_type="TaxRegistration",
                event_type="TaxRegistrationIssued",
                tax_id=tax_id,
                agent_id=agent_id,
                issue_date=date.today(),
                effective_date=date.today(),
                tax_authority=tax_authority,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "agent_id": str(agent_id),
                    "command_name": "IssueTaxRegistration",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Tax registration issued: {tax_id}")
        except Exception as e:
            logger.error(f"Error issuing tax registration: {e}")
            raise
