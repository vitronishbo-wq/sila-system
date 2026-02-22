"""Domain models do módulo IAM"""

from .enums.user_status import (
    UserStatus,
    RoleType,
    PermissionScope,
    ActionType,
    ResourceType,
    AuditAction,
    MFAType
)
from .value_objects.email import Email, EmailAddress
from .value_objects.password import Password, PasswordPolicy, PasswordResetToken
from .value_objects.token import Token, TokenPair, RefreshToken
from .models.permission import Permission, PermissionSet
from .models.role import Role, RoleSet
from .models.user import User
from .models.session import Session
from .models.audit_log import AuditLog

__all__ = [
    # Enums
    "UserStatus",
    "RoleType",
    "PermissionScope",
    "ActionType",
    "ResourceType",
    "AuditAction",
    "MFAType",
    
    # Value Objects
    "Email",
    "EmailAddress",
    "Password",
    "PasswordPolicy",
    "PasswordResetToken",
    "Token",
    "TokenPair",
    "RefreshToken",
    
    # Models
    "Permission",
    "PermissionSet",
    "Role",
    "RoleSet",
    "User",
    "Session",
    "AuditLog"
]
