"""
FastAPI routes for Event Sourcing queries.
Provides endpoints for querying event streams and audit trails.
"""
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID
import logging
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.api.schemas.events import EventResponse, EventListResponse, EventStreamResponse, HealthCheckResponse, ErrorResponse
from app.infrastructure.event_sourcing.event_store import EventStore
from app.infrastructure.event_sourcing.factory import EventStoreFactory
logger = logging.getLogger(__name__)

async def get_event_store(session: AsyncSession=Depends(get_db)) -> EventStore:
    """
    Dependency injection function for EventStore.
    Provides the configured EventStore implementation.
    
    Args:
        session: Database session
        
    Returns:
        EventStore instance
    """
    try:
        from core.db import async_session_factory
        return EventStoreFactory.get_event_store(async_session_factory)
    except Exception as e:
        logger.error(f'Failed to get EventStore: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to initialize event store')
router = APIRouter(prefix='/api/v1/events', tags=['events'])

@router.get('/aggregates/{aggregate_id}', response_model=EventStreamResponse, summary='Get event stream for an aggregate', description='Retrieves all events for a specific aggregate, enabling event sourcing replay', responses={200: {'description': 'Event stream retrieved successfully'}, 404: {'description': 'Aggregate not found'}, 500: {'description': 'Internal server error'}})
async def get_aggregate_events(aggregate_id: UUID, event_store: EventStore=Depends(get_event_store)) -> EventStreamResponse:
    """
    Get all events for a specific aggregate.
    
    This endpoint retrieves the complete event stream for an aggregate,
    which can be used for event sourcing (replay) or audit trails.
    
    Args:
        aggregate_id: UUID of the aggregate
        event_store: Injected EventStore dependency
        
    Returns:
        EventStreamResponse with all events for the aggregate
        
    Raises:
        HTTPException: If aggregate not found or database error occurs
    """
    try:
        events = await event_store.get_events_for_aggregate(aggregate_id)
        if not events:
            return EventStreamResponse(aggregate_id=aggregate_id, aggregate_type='Unknown', events=[], event_count=0)
        event_responses = [EventResponse(event_id=event.event_id, aggregate_id=event.aggregate_id, aggregate_type=event.aggregate_type, event_type=event.event_type, version=event.version, timestamp=event.timestamp, event_data=event.to_dict() if hasattr(event, 'to_dict') else {}, metadata=event.metadata, created_at=getattr(event, 'created_at', None)) for event in events]
        aggregate_type = events[0].aggregate_type if events else 'Unknown'
        return EventStreamResponse(aggregate_id=aggregate_id, aggregate_type=aggregate_type, events=event_responses, event_count=len(event_responses))
    except Exception as e:
        logger.error(f'Error fetching aggregate events: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to retrieve event stream')

@router.get('/type/{event_type}', response_model=EventListResponse, summary='Query events by type', description='Retrieves events of a specific type with optional date filtering', responses={200: {'description': 'Events retrieved successfully'}, 400: {'description': 'Invalid query parameters'}, 500: {'description': 'Internal server error'}})
async def get_events_by_type(event_type: str, from_date: Optional[datetime]=Query(None, description='Start date (ISO format)'), to_date: Optional[datetime]=Query(None, description='End date (ISO format)'), limit: int=Query(100, ge=1, le=1000, description='Maximum events to return'), offset: int=Query(0, ge=0, description='Number of events to skip'), event_store: EventStore=Depends(get_event_store)) -> EventListResponse:
    """
    Query events by type with optional date filtering.
    
    This endpoint is useful for compliance audits, domain event analysis,
    and event-driven integrations.
    
    Args:
        event_type: The event type to query (e.g., "CitizenCreated")
        from_date: Optional start date for filtering (UTC)
        to_date: Optional end date for filtering (UTC)
        limit: Maximum events to return (1-1000)
        offset: Number of events to skip for pagination
        event_store: Injected EventStore dependency
        
    Returns:
        EventListResponse with matching events
        
    Raises:
        HTTPException: If query is invalid or database error occurs
    """
    try:
        if from_date and from_date.tzinfo is None:
            from_date = from_date.replace(tzinfo=timezone.utc)
        if to_date and to_date.tzinfo is None:
            to_date = to_date.replace(tzinfo=timezone.utc)
        events = await event_store.get_events_by_type(event_type=event_type, from_date=from_date, to_date=to_date)
        paginated_events = events[offset:offset + limit]
        event_responses = [EventResponse(event_id=event.event_id, aggregate_id=event.aggregate_id, aggregate_type=event.aggregate_type, event_type=event.event_type, version=event.version, timestamp=event.timestamp, event_data=event.to_dict() if hasattr(event, 'to_dict') else {}, metadata=event.metadata, created_at=getattr(event, 'created_at', None)) for event in paginated_events]
        return EventListResponse(events=event_responses, total=len(events), limit=limit, offset=offset)
    except Exception as e:
        logger.error(f'Error querying events by type: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to query events by type')

@router.get('', response_model=EventListResponse, summary='Get all events (audit trail)', description='Retrieves events with pagination for system-wide audit trail', responses={200: {'description': 'Events retrieved successfully'}, 400: {'description': 'Invalid pagination parameters'}, 500: {'description': 'Internal server error'}})
async def get_all_events(limit: int=Query(100, ge=1, le=1000, description='Maximum events to return'), offset: int=Query(0, ge=0, description='Number of events to skip'), event_store: EventStore=Depends(get_event_store)) -> EventListResponse:
    """
    Get all events with pagination (audit trail).
    
    This is useful for compliance reporting and system auditing.
    Events are returned in chronological order.
    
    Args:
        limit: Maximum events to return per page (1-1000)
        offset: Number of events to skip for pagination
        event_store: Injected EventStore dependency
        
    Returns:
        EventListResponse with paginated events
        
    Raises:
        HTTPException: If query is invalid or database error occurs
    """
    try:
        all_events = await event_store.get_all_events(limit=offset + limit * 2)
        if not all_events:
            return EventListResponse(events=[], total=0, limit=limit, offset=offset)
        paginated_events = all_events[offset:offset + limit]
        event_responses = [EventResponse(event_id=event.event_id, aggregate_id=event.aggregate_id, aggregate_type=event.aggregate_type, event_type=event.event_type, version=event.version, timestamp=event.timestamp, event_data=event.to_dict() if hasattr(event, 'to_dict') else {}, metadata=event.metadata, created_at=getattr(event, 'created_at', None)) for event in paginated_events]
        return EventListResponse(events=event_responses, total=len(all_events), limit=limit, offset=offset)
    except Exception as e:
        logger.error(f'Error fetching all events: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to retrieve events')

@router.get('/{event_id}', response_model=EventResponse, summary='Get a specific event', description='Retrieves a single event by its ID', responses={200: {'description': 'Event retrieved successfully'}, 404: {'description': 'Event not found'}, 500: {'description': 'Internal server error'}})
async def get_event_by_id(event_id: UUID, event_store: EventStore=Depends(get_event_store)) -> EventResponse:
    """
    Get a specific event by its ID.
    
    Args:
        event_id: UUID of the event to retrieve
        event_store: Injected EventStore dependency
        
    Returns:
        EventResponse with the event details
        
    Raises:
        HTTPException: If event not found or database error occurs
    """
    try:
        event = await event_store.get_event_by_id(event_id)
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Event {event_id} not found')
        return EventResponse(event_id=event.event_id, aggregate_id=event.aggregate_id, aggregate_type=event.aggregate_type, event_type=event.event_type, version=event.version, timestamp=event.timestamp, event_data=event.to_dict() if hasattr(event, 'to_dict') else {}, metadata=event.metadata, created_at=getattr(event, 'created_at', None))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Error fetching event: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to retrieve event')

@router.post('/health', response_model=HealthCheckResponse, summary='Event store health check', description='Verifies that the event store is accessible and operational', responses={200: {'description': 'Event store is healthy'}, 503: {'description': 'Event store is unavailable'}})
async def health_check(event_store: EventStore=Depends(get_event_store)) -> HealthCheckResponse:
    """
    Check the health status of the event store.
    
    This endpoint performs a connectivity check with the event store
    and returns its operational status.
    
    Returns:
        HealthCheckResponse with status information
        
    Raises:
        HTTPException: If event store is unavailable
    """
    try:
        is_healthy = await event_store.health_check()
        event_store_type = 'postgres' if hasattr(event_store, 'session_factory') else 'memory'
        if is_healthy:
            return HealthCheckResponse(status='healthy', event_store_type=event_store_type, message='Event store is operational')
        else:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Event store health check failed')
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Health check failed: {e}')
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Event store is unavailable')
__all__ = ['router']