from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from ...domain.enums import RequestChannel, RequestPriority, ServiceType
from ...domain.models.service_request import ServiceRequest


class RequestServicePort(ABC):
    """Interface do serviço de pedidos"""

    @abstractmethod
    def create_request(
        self,
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
        """Cria um novo pedido"""
        pass

    @abstractmethod
    def get_request(
        self, request_id: UUID, user_id: UUID, is_citizen: bool = False
    ) -> ServiceRequest | None:
        """Busca pedido por ID com verificação de permissão"""
        pass

    @abstractmethod
    def list_citizen_requests(
        self, citizen_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[ServiceRequest]:
        """Lista pedidos de um cidadão"""
        pass

    @abstractmethod
    def list_operator_requests(
        self, user_id: UUID, status: str | None = None, skip: int = 0, limit: int = 100
    ) -> list[ServiceRequest]:
        """Lista pedidos atribuídos a um operador"""
        pass

    @abstractmethod
    def submit_request(self, request_id: UUID, submitted_by: UUID) -> ServiceRequest:
        """Submete um pedido (rascunho -> submetido)"""
        pass

    @abstractmethod
    def assign_request(
        self, request_id: UUID, assigned_to: UUID, assigned_by: UUID
    ) -> ServiceRequest:
        """Atribui um pedido a um operador"""
        pass

    @abstractmethod
    def change_status(
        self, request_id: UUID, new_status: str, changed_by: UUID, reason: str | None = None
    ) -> ServiceRequest:
        """Altera o status de um pedido"""
        pass

    @abstractmethod
    def link_workflow(self, request_id: UUID, workflow_instance_id: UUID) -> ServiceRequest:
        """Vincula workflow ao pedido"""
        pass
