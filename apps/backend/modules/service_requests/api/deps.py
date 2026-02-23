from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID

from app.core.database import get_session
from app.api.deps import get_notification_service
from app.core.notifications.services.notification_service import NotificationService
from ..application.services.request_service import RequestService


class RequestPermissions:
    """Verificações de permissão para pedidos"""
    
    @staticmethod
    def can_view_request(request_citizen_id: UUID, identity) -> bool:
        """Verifica se pode visualizar pedido"""
        if identity.is_superuser:
            return True
        
        if identity.is_citizen and identity.citizen_id == str(request_citizen_id):
            return True
        
        if identity.has_permission("service_request", "view"):
            return True
        
        return False
    
    @staticmethod
    def can_update_request(request, identity) -> bool:
        """Verifica se pode atualizar pedido"""
        if identity.is_superuser:
            return True
        
        # Operador atribuído
        if request.assigned_to_user_id and str(request.assigned_to_user_id) == identity.user_id:
            return True
        
        if identity.has_permission("service_request", "update"):
            return True
        
        return False
    
    @staticmethod
    def can_assign_request(identity) -> bool:
        """Verifica se pode atribuir pedidos"""
        return identity.is_superuser or identity.has_permission("service_request", "assign")


async def get_request_service(
    db: AsyncSession = Depends(get_session),
    notification_service: NotificationService = Depends(get_notification_service)
) -> RequestService:
    """Dependency para obter serviço de pedidos (ASYNC)"""
    return RequestService(db, notification_service=notification_service)


async def get_request_or_404(
    request_id: UUID,
    service: RequestService = Depends(get_request_service),
    identity = Depends(lambda: None)  # Will be set in router
):
    """Dependency para buscar pedido com verificação de acesso"""
    request = await service.get_request(request_id, UUID(identity.user_id) if identity else request_id, 
                                   identity.is_citizen if identity else False)
    
    if not request:
        from app.core.exceptions import RequestNotFoundError
        raise RequestNotFoundError(request_id).to_http_exception()
    
    return request


def require_request_permission(permission: str):
    """Dependency para verificar permissão em pedido"""
    async def decorator(
        request = Depends(get_request_or_404),
        identity = Depends(lambda: None)  # Will be set in router
    ):
        from app.core.exceptions import AccessDeniedError
        
        if permission == "view":
            if identity and not RequestPermissions.can_view_request(request.citizen_id, identity):
                raise AccessDeniedError("acessar este pedido").to_http_exception()
        elif permission == "update":
            if identity and not RequestPermissions.can_update_request(request, identity):
                raise AccessDeniedError("modificar este pedido").to_http_exception()
        elif permission == "assign":
            if identity and not RequestPermissions.can_assign_request(identity):
                raise AccessDeniedError("atribuir pedidos").to_http_exception()
        
        return request
    return decorator
