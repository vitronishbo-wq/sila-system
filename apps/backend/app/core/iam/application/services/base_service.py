from typing import Optional, TypeVar, Generic
from sqlalchemy.orm import Session
import logging
from datetime import datetime

from ...infrastructure.repositories.user_repository import UserRepository
from ...infrastructure.repositories.role_repository import RoleRepository
from ...infrastructure.repositories.permission_repository import PermissionRepository
from ...infrastructure.repositories.session_repository import SessionRepository
from ...infrastructure.repositories.audit_repository import AuditRepository
from ...infrastructure.security.password_hasher import Argon2PasswordHasher
from ...infrastructure.security.jwt_provider import JWTProvider
from ...infrastructure.security.permission_resolver import PermissionResolver

T = TypeVar('T')


class BaseService(Generic[T]):
    """Classe base para todos os serviços IAM"""
    
    def __init__(self, db: Session):
        self.db = db
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Repositórios
        self.user_repo = UserRepository(db)
        self.role_repo = RoleRepository(db)
        self.permission_repo = PermissionRepository(db)
        self.session_repo = SessionRepository(db)
        self.audit_repo = AuditRepository(db)
        
        # Segurança
        self.hasher = Argon2PasswordHasher()
        self.jwt_provider = JWTProvider()
        
        # Resolvedor de permissões (será inicializado depois)
        self.permission_resolver = None
    
    def _init_permission_resolver(self):
        """Inicializa resolvedor de permissões (lazy)"""
        if not self.permission_resolver:
            self.permission_resolver = PermissionResolver(
                permission_repo=self.permission_repo,
                user_repo=self.user_repo
            )
    
    def _log_action(self, action: str, user_id: str, resource: str, 
                   resource_id: Optional[str] = None, details: Optional[dict] = None,
                   success: bool = True, error: Optional[str] = None):
        """Regista ação para auditoria"""
        try:
            from ...infrastructure.models.audit_model import AuditLogModel
            
            audit_log = AuditLogModel(
                action=action,
                resource_type=resource,
                resource_id=resource_id or "",
                user_id=user_id,
                details=details,
                success=success,
                error_message=error
            )
            
            self.db.add(audit_log)
            self.db.commit()
        except Exception as e:
            self.logger.error(f"Erro ao registar auditoria: {str(e)}")
    
    def _handle_error(self, error: Exception, context: dict = None):
        """Trata erros de forma consistente"""
        self.logger.error(f"Erro: {str(error)}", exc_info=True, extra=context or {})
        raise error


class ServiceError(Exception):
    """Exceção base para erros de serviço"""
    def __init__(self, message: str, code: str = "SERVICE_ERROR", details: dict = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(message)


class ValidationError(ServiceError):
    """Erro de validação"""
    def __init__(self, message: str, field: Optional[str] = None, details: dict = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            details={**(details or {}), "field": field} if field else details
        )


class AuthenticationError(ServiceError):
    """Erro de autenticação"""
    def __init__(self, message: str = "Credenciais inválidas"):
        super().__init__(message=message, code="AUTHENTICATION_ERROR")


class AuthorizationError(ServiceError):
    """Erro de autorização"""
    def __init__(self, message: str = "Permissão negada", required_permissions: list = None):
        details = {"required_permissions": required_permissions} if required_permissions else None
        super().__init__(message=message, code="AUTHORIZATION_ERROR", details=details)


class NotFoundError(ServiceError):
    """Recurso não encontrado"""
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            message=f"{resource} não encontrado: {resource_id}",
            code="NOT_FOUND",
            details={"resource": resource, "resource_id": resource_id}
        )


class ConflictError(ServiceError):
    """Conflito (ex: duplicidade)"""
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(
            message=message,
            code="CONFLICT",
            details={"field": field} if field else None
        )
