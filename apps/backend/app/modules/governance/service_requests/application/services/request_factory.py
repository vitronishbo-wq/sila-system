from typing import Any
from uuid import UUID

from ...domain.enums import RequestChannel, RequestPriority, ServiceRequestStatus, ServiceType
from ...domain.models.service_request import ServiceRequest


class RequestFactory:
    """Factory para criação de pedidos"""

    @classmethod
    def create_draft(
        cls,
        citizen_id: UUID,
        created_by: UUID,
        service_type: ServiceType,
        title: str,
        description: str | None = None,
        channel: RequestChannel = RequestChannel.WEB,
        priority: RequestPriority = RequestPriority.MEDIUM,
        metadata: dict[str, Any] = None,
        tags: list[str] = None,
    ) -> ServiceRequest:
        """
        Cria um pedido em rascunho
        """
        return ServiceRequest(
            citizen_id=citizen_id,
            created_by_user_id=created_by,
            service_type=service_type,
            title=title,
            description=description,
            status=ServiceRequestStatus.DRAFT,
            channel=channel,
            priority=priority,
            metadata=metadata or {},
            tags=tags or [],
        )

    @classmethod
    def create_submitted(
        cls,
        citizen_id: UUID,
        created_by: UUID,
        service_type: ServiceType,
        title: str,
        description: str | None = None,
        channel: RequestChannel = RequestChannel.WEB,
        priority: RequestPriority = RequestPriority.MEDIUM,
        metadata: dict[str, Any] = None,
        tags: list[str] = None,
    ) -> ServiceRequest:
        """
        Cria um pedido já submetido
        """
        request = cls.create_draft(
            citizen_id=citizen_id,
            created_by=created_by,
            service_type=service_type,
            title=title,
            description=description,
            channel=channel,
            priority=priority,
            metadata=metadata,
            tags=tags,
        )
        request.submit()
        return request

    @classmethod
    def from_workflow(cls, workflow_data: dict[str, Any]) -> ServiceRequest:
        """
        Cria pedido a partir de dados do workflow
        """
        return ServiceRequest(
            citizen_id=UUID(workflow_data["citizen_id"]),
            created_by_user_id=UUID(workflow_data["created_by"]),
            service_type=ServiceType(workflow_data["service_type"]),
            title=workflow_data["title"],
            description=workflow_data.get("description"),
            status=ServiceRequestStatus(
                workflow_data.get("status", ServiceRequestStatus.DRAFT.value)
            ),
            channel=RequestChannel(workflow_data.get("channel", RequestChannel.WEB.value)),
            priority=RequestPriority(workflow_data.get("priority", RequestPriority.MEDIUM.value)),
            workflow_data=workflow_data.get("workflow_data", {}),
            metadata=workflow_data.get("metadata", {}),
            tags=workflow_data.get("tags", []),
        )
