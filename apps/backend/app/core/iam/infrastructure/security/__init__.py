"""Módulo de segurança do IAM"""

from .password_hasher import (
    Argon2PasswordHasher,
    BcryptPasswordHasher,
    PasswordGenerator,
    PasswordPolicy
)
from .jwt_provider import JWTProvider, TokenBlacklist
from .permission_resolver import PermissionResolver, PermissionEvaluator, requires_permissions
from .token_blacklist import (
    RedisTokenBlacklist,
    DatabaseTokenBlacklist,
    MemoryTokenBlacklist
)
from .mfa import MFAProvider, EmailMFAProvider, SMSMFAProvider

__all__ = [
    "Argon2PasswordHasher",
    "BcryptPasswordHasher",
    "PasswordGenerator",
    "PasswordPolicy",
    "JWTProvider",
    "TokenBlacklist",
    "PermissionResolver",
    "PermissionEvaluator",
    "requires_permissions",
    "RedisTokenBlacklist",
    "DatabaseTokenBlacklist",
    "MemoryTokenBlacklist",
    "MFAProvider",
    "EmailMFAProvider",
    "SMSMFAProvider"
]
