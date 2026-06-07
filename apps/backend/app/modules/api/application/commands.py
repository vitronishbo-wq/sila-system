"""
API Module Command Handlers
Shows the pattern for API operations with event publishing.
"""

import logging
from datetime import UTC, date, datetime
from uuid import UUID

from apps.backend.app.core.events.event_bus import EventBus
from apps.backend.app.modules.api.domain.events import (
    APIAccessTokenIssued,
    APIEndpointRegistered,
    APIRequestProcessed,
)

logger = logging.getLogger(__name__)


class RegisterAPIEndpointCommandHandler:
    """Register API endpoint."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        endpoint_id: UUID,
        endpoint_path: str,
        http_method: str,
        owner_id: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Registering API endpoint {endpoint_path}")
        try:
            event = APIEndpointRegistered(
                aggregate_id=endpoint_id,
                aggregate_type="APIEndpoint",
                event_type="APIEndpointRegistered",
                endpoint_id=endpoint_id,
                endpoint_path=endpoint_path,
                http_method=http_method,
                owner_id=owner_id,
                registration_date=date.today(),
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "RegisterAPIEndpoint",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"API endpoint registered: {endpoint_id}")
        except Exception as e:
            logger.error(f"Error registering API endpoint: {e}")
            raise


class IssueAPIAccessTokenCommandHandler:
    """Issue API access token (ACAO compliance)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        token_id: UUID,
        consumer_id: UUID,
        token_value: str = "",
        expiry_days: int = 90,
        scopes: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Issuing API access token {token_id}")
        try:
            event = APIAccessTokenIssued(
                aggregate_id=token_id,
                aggregate_type="APIAccessToken",
                event_type="APIAccessTokenIssued",
                token_id=token_id,
                consumer_id=consumer_id,
                issue_date=date.today(),
                token_value=token_value,
                expiry_days=expiry_days,
                scopes=scopes,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "IssueAPIAccessToken",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"API access token issued: {token_id}")
        except Exception as e:
            logger.error(f"Error issuing API access token: {e}")
            raise


class ProcessAPIRequestCommandHandler:
    """Process API request (ACAO tracking)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        request_id: UUID,
        endpoint_id: UUID,
        consumer_id: UUID,
        status_code: int = 200,
        response_time_ms: int = 0,
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Processing API request {request_id}")
        try:
            event = APIRequestProcessed(
                aggregate_id=request_id,
                aggregate_type="APIRequest",
                event_type="APIRequestProcessed",
                request_id=request_id,
                endpoint_id=endpoint_id,
                consumer_id=consumer_id,
                processed_at=datetime.now(UTC),
                status_code=status_code,
                response_time_ms=response_time_ms,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "ProcessAPIRequest",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"API request processed: {request_id}")
        except Exception as e:
            logger.error(f"Error processing API request: {e}")
            raise
