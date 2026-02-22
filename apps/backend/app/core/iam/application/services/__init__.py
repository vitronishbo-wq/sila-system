"""Services do módulo IAM"""

from .base_service import (
    BaseService, 
    ServiceError, 
    ValidationError, 
    AuthenticationError, 
    AuthorizationError, 
    NotFoundError, 
    ConflictError
)
from .auth_service import AuthService
from .user_service import UserService
from .role_service import RoleService
from .permission_service import PermissionService
from .session_service import SessionService
from .audit_service import AuditService

__all__ = [
    "BaseService",
    "ServiceError",
    "ValidationError",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "ConflictError",
    "AuthService",
    "UserService",
    "RoleService",
    "PermissionService",
    "SessionService",
    "AuditService"
]
