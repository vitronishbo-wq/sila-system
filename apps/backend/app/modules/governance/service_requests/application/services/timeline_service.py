from apps.backend.app.core.observability import trace

"Timeline service"
from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from ..infrastructure.repositories.attachment_repository import AttachmentRepository
from ..infrastructure.repositories.event_repository import EventRepository
from ..infrastructure.repositories.request_repository import RequestRepository
from ..integrations.workflow_client import WorkflowClient


class TimelineService:
    """Aggregates events, workflow history, and attachments"""

    def __init__(
        self,
        db: AsyncSession,
        request_repo: RequestRepository,
        event_repo: EventRepository,
        attachment_repo: AttachmentRepository,
        workflow_client: WorkflowClient,
    ):
        self.db = db
        self.request_repo = request_repo
        self.event_repo = event_repo
        self.attachment_repo = attachment_repo
        self.workflow_client = workflow_client

    @trace()
    async def get_timeline(self, request_id: UUID) -> list[dict[str, Any]]:
        """Get complete request timeline"""
        timeline = []
        events = await self.event_repo.get_by_request(request_id)
        for event in events:
            timeline.append(
                {
                    "type": "EVENT",
                    "event_type": event.event_type,
                    "timestamp": event.created_at.isoformat(),
                    "actor_id": str(event.actor_id),
                    "payload": event.payload,
                }
            )
        attachments = await self.attachment_repo.get_by_request(request_id)
        for attachment in attachments:
            timeline.append(
                {
                    "type": "ATTACHMENT",
                    "filename": attachment.filename,
                    "timestamp": attachment.created_at.isoformat(),
                    "actor_id": str(attachment.uploaded_by),
                    "size_bytes": attachment.size_bytes,
                }
            )
        request = await self.request_repo.get_by_id(request_id)
        if request and request.workflow_instance_id:
            history = await self.workflow_client.get_history(request.workflow_instance_id)
            for step in history:
                timeline.append(
                    {
                        "type": "WORKFLOW",
                        "step": step.get("step_name"),
                        "timestamp": step.get("timestamp"),
                        "actor_id": step.get("actor_id"),
                    }
                )
        timeline.sort(key=lambda x: x["timestamp"])
        return timeline

    @trace()
    async def get_summary(self, request_id: UUID) -> dict[str, Any]:
        """Get request summary with latest state"""
        request = await self.request_repo.get_by_id(request_id)
        if not request:
            return {}
        events = await self.event_repo.get_recent(request_id, limit=5)
        attachments = await self.attachment_repo.get_by_request(request_id)
        return {
            "id": str(request.id),
            "status": request.status.value,
            "citizen_id": str(request.citizen_id),
            "service_type": request.service_type,
            "channel": request.channel,
            "priority": request.priority,
            "created_at": request.created_at.isoformat(),
            "updated_at": request.updated_at.isoformat() if request.updated_at else None,
            "recent_events": [e.to_dict() for e in events],
            "attachments_count": len(attachments),
            "workflow_instance_id": str(request.workflow_instance_id)
            if request.workflow_instance_id
            else None,
        }
