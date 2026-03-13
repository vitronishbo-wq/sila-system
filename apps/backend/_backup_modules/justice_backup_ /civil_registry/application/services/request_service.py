"""
Serviço REAL de pedidos do cidadão (Motor SILA)
Fase 5 - Consolidado com BaseRequestService
"""
import uuid
from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..ports.platform_shared_ports import BaseRequestService, EntityStatus, NotificationService, Request, RequestRepository
from app.models.iam_user import IamUser as User

class RequestService(BaseRequestService[Request, RequestRepository]):
    """Serviço de Pedidos - ÚNICA fonte de verdade para operações com requests"""

    def __init__(self, db: AsyncSession, **kwargs):
        notification_svc = NotificationService(db)
        super().__init__(db=db, repository=RequestRepository(db), notification_service=notification_svc, audit_enabled=True, **kwargs)

    def get_repository(self) -> RequestRepository:
        """Return repository instance"""
        return RequestRepository(self.db)

    def default_status(self) -> str:
        """Initial status for citizen requests"""
        return EntityStatus.PENDING.value

    async def create_request_model(self, citizen_id: UUID, request_data: Dict[str, Any], **kwargs) -> Request:
        """Create Request domain model (domain-specific factory)"""
        return Request(id=uuid.uuid4(), citizen_id=citizen_id, service_id=request_data.get('service_id'), service_code=request_data.get('service_code'), data_payload=request_data.get('data'), territory_id=request_data.get('territory_id'), status=self.default_status())

    async def get_user_from_citizen_id(self, citizen_id: UUID) -> Optional[UUID]:
        """Map citizen to user for notifications"""
        result = await self.db.execute(select(User).where(User.citizen_id == citizen_id))
        user = result.scalars().first()
        return user.id if user else None

    async def create_request(self, citizen_id: UUID, service_id: UUID, service_code: str, data: dict=None, territory_id: UUID=None) -> Request:
        """Cria um novo pedido administrativo para um cidadão"""
        return await super().create_request(citizen_id=citizen_id, created_by=citizen_id, request_data={'service_id': service_id, 'service_code': service_code, 'data': data, 'territory_id': territory_id})

    async def get_citizen_requests(self, citizen_id: UUID) -> List[Request]:
        """Lista todos os pedidos de um cidadão"""
        requests, _ = await super().list_citizen_requests(citizen_id)
        return requests

    async def get_request(self, request_id: UUID) -> Optional[Request]:
        """Busca detalhe de um pedido"""
        return await self.repo.get_by_id(request_id)

    async def update_state(self, request_id: UUID, new_status: EntityStatus, actor_id: str='SYSTEM') -> Optional[Request]:
        """Evolui o estado do pedido (ex: PENDING -> PROCESSING)"""
        return await super().update_status(request_id=request_id, new_status=new_status.value, updated_by=UUID(actor_id) if actor_id != 'SYSTEM' else request_id)