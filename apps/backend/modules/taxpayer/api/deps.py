from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional, List, Callable
from uuid import UUID
import logging

from core.database import get_db
from ..application.services.taxpayer_service import TaxpayerService
from ..application.services.tax_declaration_service import TaxDeclarationService
from ..application.services.tax_debt_service import TaxDebtService
from ..application.services.tax_payment_service import TaxPaymentService
from ..application.services.tax_certificate_service import TaxCertificateService
from ..application.services.agt_sync_service import AGTSyncService
from ..infrastructure.repositories import (
    TaxpayerRepository,
    AuditRepository
)
from ..infrastructure.integrations.agt_api_client import AGTApiClient
from ..infrastructure.integrations.agt_mock_client import AGTMockClient
from ..infrastructure.cache.redis_cache import RedisCache
from ..infrastructure.notifications.notification_service import NotificationService
from ..infrastructure.audit.audit_logger import AuditLogger
from ..infrastructure.audit.audit_storage import AuditStorage
from core.config import settings


logger = logging.getLogger(__name__)


# ==================== REPOSITORIES ====================

def get_taxpayer_repository(db: Session = Depends(get_db)) -> TaxpayerRepository:
    """Dependency para TaxpayerRepository"""
    return TaxpayerRepository(db)


def get_audit_storage(db: Session = Depends(get_db)) -> AuditStorage:
    """Dependency para AuditStorage"""
    return AuditStorage(db)


# ==================== INFRASTRUCTURE ====================

def get_agt_client() -> AGTApiClient:
    """Retorna cliente AGT (real ou mock baseado em configuração)"""
    if getattr(settings, 'AGT_MOCK_ENABLED', False):
        return AGTMockClient()
    return AGTApiClient()


def get_cache() -> RedisCache:
    """Dependency para RedisCache"""
    return RedisCache()


def get_notification_service() -> NotificationService:
    """Dependency para NotificationService"""
    return NotificationService()


def get_audit_logger(
    storage: AuditStorage = Depends(get_audit_storage)
) -> AuditLogger:
    """Dependency para AuditLogger"""
    return AuditLogger(storage)


# ==================== APPLICATION SERVICES ====================

def get_taxpayer_service(
    repo: TaxpayerRepository = Depends(get_taxpayer_repository),
    agt: AGTApiClient = Depends(get_agt_client),
    notification: NotificationService = Depends(get_notification_service),
    audit: AuditLogger = Depends(get_audit_logger),
    cache: RedisCache = Depends(get_cache)
) -> TaxpayerService:
    """Dependency para TaxpayerService"""
    return TaxpayerService(repo, agt, notification, audit, cache)


def get_declaration_service(
    repo: TaxpayerRepository = Depends(get_taxpayer_repository),
    agt: AGTApiClient = Depends(get_agt_client),
    notification: NotificationService = Depends(get_notification_service),
    audit: AuditLogger = Depends(get_audit_logger)
) -> TaxDeclarationService:
    """Dependency para TaxDeclarationService"""
    return TaxDeclarationService(repo, agt, notification, audit)


def get_debt_service(
    repo: TaxpayerRepository = Depends(get_taxpayer_repository),
    agt: AGTApiClient = Depends(get_agt_client),
    notification: NotificationService = Depends(get_notification_service),
    audit: AuditLogger = Depends(get_audit_logger)
) -> TaxDebtService:
    """Dependency para TaxDebtService"""
    return TaxDebtService(repo, agt, notification, audit)


def get_payment_service(
    repo: TaxpayerRepository = Depends(get_taxpayer_repository),
    agt: AGTApiClient = Depends(get_agt_client),
    notification: NotificationService = Depends(get_notification_service),
    audit: AuditLogger = Depends(get_audit_logger)
) -> TaxPaymentService:
    """Dependency para TaxPaymentService"""
    return TaxPaymentService(repo, agt, notification, audit)


def get_certificate_service(
    repo: TaxpayerRepository = Depends(get_taxpayer_repository),
    agt: AGTApiClient = Depends(get_agt_client),
    notification: NotificationService = Depends(get_notification_service),
    audit: AuditLogger = Depends(get_audit_logger)
) -> TaxCertificateService:
    """Dependency para TaxCertificateService"""
    return TaxCertificateService(repo, agt, notification, audit)


def get_agt_sync_service(
    repo: TaxpayerRepository = Depends(get_taxpayer_repository),
    agt: AGTApiClient = Depends(get_agt_client),
    audit: AuditLogger = Depends(get_audit_logger)
) -> AGTSyncService:
    """Dependency para AGTSyncService"""
    return AGTSyncService(repo, agt, audit)


# ==================== PERMISSION DEPENDENCIES ====================

def require_taxpayer_permission(permission: str) -> Callable:
    """Dependency para verificar permissão"""
    async def dependency(request: Request):
        user = getattr(request.state, "user", None)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Autenticação necessária"
            )
        
        # Superuser pode tudo
        if user.get("is_superuser"):
            return True
        
        permissions = user.get("permissions", [])
        if permission not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permissão necessária: {permission}"
            )
        return True
    return dependency


def can_access_taxpayer(taxpayer_id: UUID):
    """Dependency para verificar acesso a contribuinte"""
    async def dependency(
        request: Request,
        service: TaxpayerService = Depends(get_taxpayer_service)
    ):
        user = getattr(request.state, "user", None)
        user_id = getattr(request.state, "user_id", None)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Autenticação necessária"
            )
        
        # Superuser pode tudo
        if user.get("is_superuser"):
            return taxpayer_id
        
        # Operador pode acessar qualquer contribuinte
        if "operator" in user.get("roles", []):
            return taxpayer_id
        
        # Cidadão só pode acessar próprio NIF
        citizen_id = user.get("citizen_id")
        if citizen_id:
            try:
                taxpayer = await service.get_taxpayer(taxpayer_id)
                if taxpayer and str(taxpayer.get("id")) == citizen_id:
                    return taxpayer_id
            except:
                pass
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado a este contribuinte"
        )
    return dependency


# ==================== CURRENT USER ====================

def get_current_user(request: Request) -> dict:
    """Obtém usuário autenticado da requisição"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticação necessária"
        )
    return user


def get_current_user_optional(request: Request) -> Optional[dict]:
    """Obtém usuário autenticado (opcional)"""
    return getattr(request.state, "user", None)
