from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from ..enums import RequestChannel, RequestPriority, ServiceRequestStatus, ServiceType


@dataclass
class ServiceRequest:
    """Pedido de serviço (Aggregate Root)"""

    id: UUID = field(default_factory=uuid4)
    request_number: str | None = None
    citizen_id: UUID = field(default_factory=uuid4)
    created_by: UUID | None = None
    created_by_user_id: UUID = field(default_factory=uuid4)
    assigned_to_user_id: UUID | None = None
    service_type: ServiceType = ServiceType.GENERAL_SUPPORT
    title: str = ""
    description: str | None = None
    status: ServiceRequestStatus = ServiceRequestStatus.DRAFT
    priority: RequestPriority = RequestPriority.MEDIUM
    channel: RequestChannel = RequestChannel.WEB
    workflow_instance_id: UUID | None = None
    workflow_data: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime | None = None
    submitted_at: datetime | None = None
    completed_at: datetime | None = None
    deadline: datetime | None = None
    sla_due_at: datetime | None = None
    sla_breached: bool = False

    def __post_init__(self):
        if self.created_by is not None:
            self.created_by_user_id = self.created_by
        if isinstance(self.service_type, str):
            legacy_service_map = {
                "DOCUMENT_REQUEST": ServiceType.IDENTITY_BI,
                "GENERAL": ServiceType.GENERAL_SUPPORT,
                "DOCUMENT": ServiceType.IDENTITY_BI,
            }
            value = legacy_service_map.get(self.service_type, self.service_type)
            self.service_type = ServiceType(value)
        if isinstance(self.status, str):
            self.status = ServiceRequestStatus(self.status)
        if isinstance(self.priority, str):
            legacy_priority_map = {
                "NORMAL": RequestPriority.MEDIUM,
                "MEDIUM": RequestPriority.MEDIUM,
                "LOW": RequestPriority.LOW,
                "HIGH": RequestPriority.HIGH,
                "URGENT": RequestPriority.URGENT,
                "CRITICAL": RequestPriority.CRITICAL,
            }
            value = legacy_priority_map.get(self.priority, self.priority)
            self.priority = RequestPriority(value)
        if isinstance(self.channel, str):
            self.channel = RequestChannel(self.channel)

    @property
    def is_draft(self) -> bool:
        return self.status == ServiceRequestStatus.DRAFT

    @property
    def is_active(self) -> bool:
        return self.status in ServiceRequestStatus.active_statuses()

    @property
    def is_terminal(self) -> bool:
        return self.status in ServiceRequestStatus.terminal_statuses()

    def submit(self):
        """Submete o pedido"""
        if self.status != ServiceRequestStatus.DRAFT:
            raise ValueError(f"Não é possível submeter pedido com status {self.status}")
        self.status = ServiceRequestStatus.SUBMITTED
        self.submitted_at = datetime.now()
        self.updated_at = datetime.now()

    def assign(self, user_id: UUID, assigned_by: UUID):
        """Atribui pedido a um operador"""
        self.assigned_to_user_id = user_id
        self.updated_at = datetime.now()
        self.metadata["assigned_by"] = str(assigned_by)
        self.metadata["assigned_at"] = datetime.now().isoformat()

    def change_status(
        self, new_status: ServiceRequestStatus, changed_by: UUID, reason: str | None = None
    ):
        """Altera status do pedido"""
        old_status = self.status
        self.status = new_status
        self.updated_at = datetime.now()
        if new_status == ServiceRequestStatus.COMPLETED:
            self.completed_at = datetime.now()
        if "status_history" not in self.metadata:
            self.metadata["status_history"] = []
        self.metadata["status_history"].append(
            {
                "from": old_status.value,
                "to": new_status.value,
                "by": str(changed_by),
                "at": datetime.now().isoformat(),
                "reason": reason,
            }
        )

    def link_workflow(self, workflow_instance_id: UUID):
        """Vincula instância de workflow"""
        self.workflow_instance_id = workflow_instance_id
        self.updated_at = datetime.now()

    def update_workflow_data(self, key: str, value: Any):
        """Atualiza dados do workflow"""
        self.workflow_data[key] = value
        self.updated_at = datetime.now()

    def add_tag(self, tag: str):
        """Adiciona tag"""
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str):
        """Remove tag"""
        if tag in self.tags:
            self.tags.remove(tag)

    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            "id": str(self.id),
            "request_number": self.request_number,
            "citizen_id": str(self.citizen_id),
            "created_by_user_id": str(self.created_by_user_id),
            "assigned_to_user_id": str(self.assigned_to_user_id)
            if self.assigned_to_user_id
            else None,
            "service_type": self.service_type.value,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "channel": self.channel.value,
            "workflow_instance_id": str(self.workflow_instance_id)
            if self.workflow_instance_id
            else None,
            "workflow_data": self.workflow_data,
            "metadata": self.metadata,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "submitted_at": self.submitted_at.isoformat() if self.submitted_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "sla_due_at": self.sla_due_at.isoformat() if self.sla_due_at else None,
            "sla_breached": self.sla_breached,
            "is_active": self.is_active,
            "is_draft": self.is_draft,
            "is_terminal": self.is_terminal,
        }
