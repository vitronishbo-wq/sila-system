from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.services.base_request_service import BaseRequestService
from ...domain.models.identity_request import IdentityRequest, RequestStatus
from ...infrastructure.repositories.identity_request_repository import IdentityRequestRepository

class IdentityRequestService(BaseRequestService[IdentityRequest, IdentityRequestRepository]):
    """Serviço unificado para processos de identidade (BI, Atestados)."""
    
    def __init__(self, db: AsyncSession, notification_service=None):
        super().__init__(
            db=db,
            repository=IdentityRequestRepository(db),
            notification_service=notification_service,
            audit_enabled=True
        )
    
    def get_repository(self) -> IdentityRequestRepository:
        return IdentityRequestRepository(self.db)
    
    def default_status(self) -> str:
        return RequestStatus.PENDING.value
    
    async def create_request_model(
        self,
        citizen_id: UUID,
        request_data: Dict[str, Any],
        **kwargs
    ) -> IdentityRequest:
        """Instancia um IdentityRequest."""
        service_code = request_data.get("service_code", "000")
        req = IdentityRequest(
            citizen_fuc_id=str(citizen_id),
            service_code=service_code
        )
        if "bi_id" in request_data:
            req.bi_id = request_data["bi_id"]
            
        return req
    
    async def get_user_from_citizen_id(self, citizen_id: UUID) -> Optional[UUID]:
        """No SILA, citizen_id costuma ser o próprio user_id no namespace do cidadão."""
        return citizen_id

    # Extensões específicas do domínio de Identidade
    async def add_note(self, request_id: UUID, operator: str, text: str):
        request = await self.repo.get_by_id(request_id)
        if not request:
            raise ValueError("Pedido não encontrado")
        
        request.add_note(operator, text)
        return await self.repo.save(request)

    async def transition(self, request_id: UUID, new_status: RequestStatus, reason: str = None, updated_by: UUID = None):
        """Atualiza estado com auditoria e notificações da base."""
        # Se não houver updated_by, assume SYSTEM ou o próprio ID (compatibilidade)
        actor = updated_by or UUID("00000000-0000-0000-0000-000000000000")
        
        return await self.update_status(
            request_id=request_id,
            new_status=new_status.value,
            updated_by=actor,
            reason=reason
        )
