from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from ...domain.enums import ServiceRequestStatus, ServiceType
from ...domain.models.service_request import ServiceRequest


class RequestRepositoryPort(ABC):
    """Interface do repositório de pedidos"""

    @abstractmethod
    async def save(self, request: ServiceRequest) -> ServiceRequest:
        """Salva um pedido"""
        pass

    @abstractmethod
    async def get_by_id(self, request_id: UUID) -> ServiceRequest | None:
        """Busca pedido por ID"""
        pass

    @abstractmethod
    async def get_by_number(self, request_number: str) -> ServiceRequest | None:
        """Busca pedido por número"""
        pass

    @abstractmethod
    async def get_by_citizen(
        self, citizen_id: UUID, skip: int = 0, limit: int = 100
    ) -> tuple[list[ServiceRequest], int]:
        """Busca pedidos por cidadão"""
        pass

    @abstractmethod
    async def get_by_assignee(
        self,
        user_id: UUID,
        status: ServiceRequestStatus | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[ServiceRequest], int]:
        """Busca pedidos atribuídos a um usuário"""
        pass

    @abstractmethod
    async def get_by_status(
        self, status: ServiceRequestStatus, skip: int = 0, limit: int = 100
    ) -> tuple[list[ServiceRequest], int]:
        """Busca pedidos por status"""
        pass

    @abstractmethod
    async def get_by_service_type(
        self, service_type: ServiceType, skip: int = 0, limit: int = 100
    ) -> tuple[list[ServiceRequest], int]:
        """Busca pedidos por tipo de serviço"""
        pass

    @abstractmethod
    async def get_by_date_range(
        self, start_date: datetime, end_date: datetime, skip: int = 0, limit: int = 100
    ) -> tuple[list[ServiceRequest], int]:
        """Busca pedidos por intervalo de datas"""
        pass

    @abstractmethod
    async def search(
        self, query: str, filters: dict = None, skip: int = 0, limit: int = 100
    ) -> tuple[list[ServiceRequest], int]:
        """Pesquisa avançada de pedidos"""
        pass

    @abstractmethod
    async def count_by_status(self) -> dict:
        """Contagem de pedidos por status"""
        pass

    @abstractmethod
    async def get_next_sequence(self, year: int) -> int:
        """Próximo número sequencial do ano"""
        pass
