"""
Serviço REAL de pedidos do cidadão (Motor SILA)
Fase 5 - Consolidado com BaseRequestService
"""
import uuid
from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.services.base_request_service import BaseRequestService
from app.core.workflow.models.request import Request
from app.core.workflow.infrastructure.repositories.request_repository import RequestRepository
from app.core.constants import EntityStatus
from app.core.notifications.services.notification_service import NotificationService
from app.core.iam.models.user import User


class RequestService(BaseRequestService[Request, RequestRepository]):
    """Serviço de Pedidos - ÚNICA fonte de verdade para operações com requests"""

    def __init__(self, db: AsyncSession, **kwargs):
        notification_svc = NotificationService(db)
        super().__init__(
            db=db,
            repository=RequestRepository(db),
            notification_service=notification_svc,
            audit_enabled=True,
            **kwargs
        )

    # ========== Abstract Methods Implementation ==========
    
    def get_repository(self) -> RequestRepository:
        """Return repository instance"""
        return RequestRepository(self.db)
    
    def default_status(self) -> str:
        """Initial status for citizen requests"""
        return EntityStatus.PENDING.value
    
    async def create_request_model(
        self,
        citizen_id: UUID,
        request_data: Dict[str, Any],
        **kwargs
    ) -> Request:
        """Create Request domain model (domain-specific factory)"""
        return Request(
            id=uuid.uuid4(),
            citizen_id=citizen_id,
            service_id=request_data.get("service_id"),
            service_code=request_data.get("service_code"),
            data_payload=request_data.get("data"),
            territory_id=request_data.get("territory_id"),
            status=self.default_status()
        )
    
    async def get_user_from_citizen_id(self, citizen_id: UUID) -> Optional[UUID]:
        """Map citizen to user for notifications"""
        result = await self.db.execute(
            select(User).where(User.citizen_id == citizen_id)
        )
        user = result.scalars().first()
        return user.id if user else None
    
    # ========== Public API Methods (Backward Compatible) ==========
    
    async def create_request(
        self,
        citizen_id: UUID,
        service_id: UUID,
        service_code: str,
        data: dict = None,
        territory_id: UUID = None
    ) -> Request:
        """Cria um novo pedido administrativo para um cidadão"""
        # Delegate to base template method (no API change)
        return await super().create_request(
            citizen_id=citizen_id,
            created_by=citizen_id,  # Convert for base signature
            request_data={
                "service_id": service_id,
                "service_code": service_code,
                "data": data,
                "territory_id": territory_id,
            }
        )

    async def get_citizen_requests(self, citizen_id: UUID) -> List[Request]:
        """Lista todos os pedidos de um cidadão"""
        requests, _ = await super().list_citizen_requests(citizen_id)
        return requests

    async def get_request(self, request_id: UUID) -> Optional[Request]:
        """Busca detalhe de um pedido"""
        # For single request retrieval without permission check
        return await self.repo.get_by_id(request_id)

    async def update_state(
        self,
        request_id: UUID,
        new_status: EntityStatus,
        actor_id: str = "SYSTEM"
    ) -> Optional[Request]:
        """Evolui o estado do pedido (ex: PENDING -> PROCESSING)"""
        # Delegate to base update_status (audit + notification automatic)
        return await super().update_status(
            request_id=request_id,
            new_status=new_status.value,
            updated_by=UUID(actor_id) if actor_id != "SYSTEM" else request_id
        )
