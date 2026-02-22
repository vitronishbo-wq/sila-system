"""Módulo IAM - Identity and Access Management"""

# Re-export do domain para conveniência
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
