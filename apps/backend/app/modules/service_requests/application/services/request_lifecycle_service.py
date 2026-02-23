from app.core.observability import trace
"""Request lifecycle service"""
from uuid import UUID
from typing import Optional, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from ..domain.models.service_request import ServiceRequest
from ..domain.models.request_event import RequestEvent
from ..infrastructure.repositories.request_repository import RequestRepository
from ..infrastructure.repositories.event_repository import EventRepository
from ..integrations.workflow_client import WorkflowClient
from ..domain.enums import RequestStatus


class RequestLifecycleService:
    """Manages request lifecycle from creation to closure"""

    def __init__(
        self,
        db: AsyncSession,
        request_repo: RequestRepository,
        event_repo: EventRepository,
        workflow_client: WorkflowClient,
    ):
        self.db = db
        self.request_repo = request_repo
        self.event_repo = event_repo
        self.workflow_client = workflow_client

    @trace()
    async def create_request(
        self,
        citizen_id: UUID,
        created_by: UUID,
        service_type: str,
        channel: str,
        priority: str,
        metadata: Dict[str, Any],
    ) -> ServiceRequest:
        """Create new request and start workflow"""
        # Create request
        request = ServiceRequest(
            citizen_id=citizen_id,
            created_by=created_by,
            service_type=service_type,
            channel=channel,
            priority=priority,
            status=RequestStatus.RECEIVED,
            metadata=metadata,
        )
        
        # Save request
        saved = await self.request_repo.save(request)
        
        # Start workflow
        workflow_response = await self.workflow_client.start_workflow(
            definition_key="SERVICE_REQUEST_WORKFLOW",
            business_key=str(saved.id),
            variables={
                "service_type": service_type,
                "priority": priority,
                "citizen_id": str(citizen_id),
            },
            actor_id=created_by,
        )
        
        if workflow_response:
            saved.workflow_instance_id = UUID(workflow_response["instance_id"])
            saved = await self.request_repo.save(saved)
        
        # Record event
        event = RequestEvent(
            request_id=saved.id,
            event_type="CREATED",
            payload={
                "service_type": service_type,
                "channel": channel,
                "priority": priority,
            },
            actor_id=created_by,
        )
        await self.event_repo.save(event)
        
        if workflow_response:
            workflow_event = RequestEvent(
                request_id=saved.id,
                event_type="WORKFLOW_STARTED",
                payload={"workflow_instance_id": str(workflow_response["instance_id"])},
                actor_id=created_by,
            )
            await self.event_repo.save(workflow_event)
        
        return saved

    @trace()
    async def transition_request(
        self,
        request_id: UUID,
        transition: str,
        actor_id: UUID,
        data: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Execute workflow transition"""
        request = await self.request_repo.get_by_id(request_id)
        if not request or not request.workflow_instance_id:
            return False
        
        # Send transition to workflow
        success = await self.workflow_client.send_transition(
            request.workflow_instance_id,
            transition,
            actor_id,
            data,
        )
        
        if success:
            # Record state change event
            event = RequestEvent(
                request_id=request_id,
                event_type="STATE_CHANGED",
                payload={"transition": transition, "data": data or {}},
                actor_id=actor_id,
            )
            await self.event_repo.save(event)
        
        return success

    @trace()
    async def close_request(
        self,
        request_id: UUID,
        actor_id: UUID,
        resolution: str,
    ) -> bool:
        """Close request"""
        request = await self.request_repo.get_by_id(request_id)
        if not request:
            return False
        
        request.status = RequestStatus.CLOSED
        request.metadata["resolution"] = resolution
        
        await self.request_repo.save(request)
        
        # Record event
        event = RequestEvent(
            request_id=request_id,
            event_type="CLOSED",
            payload={"resolution": resolution},
            actor_id=actor_id,
        )
        await self.event_repo.save(event)
        
        return True
