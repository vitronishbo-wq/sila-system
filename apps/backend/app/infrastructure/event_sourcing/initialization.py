"""
Event Store Initialization and Migration Helper
Handles schema creation and cleanup for event store tables
"""

import logging

from sqlalchemy import exc, text
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.infrastructure.event_sourcing.migrations import (
    CREATE_EVENT_STORE_TABLE,
    CREATE_INDEXES,
    DROP_EVENT_STORE_TABLE,
)

logger = logging.getLogger(__name__)


async def init_event_store(session: AsyncSession) -> bool:
    """
    Initialize the event store schema.
    Creates the event_store table and indexes if they don't exist.

    Args:
        session: AsyncSession for database operations

    Returns:
        True if successful, False otherwise
    """
    try:
        await session.execute(text(CREATE_EVENT_STORE_TABLE))
        await session.commit()
        logger.debug("✓ Event store table created")
        for index_sql in CREATE_INDEXES:
            try:
                await session.execute(text(index_sql))
                await session.commit()
            except exc.SQLAlchemyError as e:
                logger.warning(f"Index creation statement may have failed (non-fatal): {e}")
                await session.rollback()
        logger.info("✓ Event store table and indexes initialized successfully")
        return True
    except exc.SQLAlchemyError as e:
        logger.error(f"Failed to initialize event store: {e}")
        await session.rollback()
        return False


async def drop_event_store(session: AsyncSession) -> bool:
    """
    Drop the event store table (for cleanup/testing).

    Args:
        session: AsyncSession for database operations

    Returns:
        True if successful, False otherwise
    """
    try:
        await session.execute(text(DROP_EVENT_STORE_TABLE))
        await session.commit()
        logger.info("✓ Event store table dropped")
        return True
    except exc.SQLAlchemyError as e:
        logger.error(f"Failed to drop event store: {e}")
        await session.rollback()
        return False


async def event_store_health_check(session: AsyncSession) -> bool:
    """
    Check if event store is healthy and accessible.

    Args:
        session: AsyncSession for database operations

    Returns:
        True if event store is accessible
    """
    try:
        await session.execute(text("SELECT 1 FROM event_store LIMIT 1;"))
        return True
    except exc.SQLAlchemyError:
        return False


__all__ = ["init_event_store", "drop_event_store", "event_store_health_check"]
