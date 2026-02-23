from enum import Enum


class UserStatus(str, Enum):
    """Status do utilizador no sistema"""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    BLOCKED = "BLOCKED"
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    PASSWORD_EXPIRED = "PASSWORD_EXPIRED"
    LOCKED = "LOCKED"  # Múltiplas tentativas falhas
    
    @classmethod
    def active_statuses(cls):
        return [cls.ACTIVE]
    
    @classmethod
    def inactive_statuses(cls):
        return [cls.INACTIVE, cls.BLOCKED, cls.LOCKED]


class RoleType(str, Enum):
    """Tipos de roles no sistema"""
    SYSTEM = "SYSTEM"  # Roles internas do sistema (não editáveis)
    CUSTOM = "CUSTOM"  # Roles criadas por administradores
    HIERARCHICAL = "HIERARCHICAL"  # Roles baseadas em hierarquia


class PermissionScope(str, Enum):
    """Escopo da permissão"""
    OWN = "OWN"  # Apenas recursos próprios
    UNIT = "UNIT"  # Recursos da unidade/departamento
    PROVINCE = "PROVINCE"  # Recursos da província
    NATIONAL = "NATIONAL"  # Todos os recursos


class ActionType(str, Enum):
    """Tipos de ações em recursos"""
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    ISSUE = "ISSUE"
    CANCEL = "CANCEL"
    EXPORT = "EXPORT"
    IMPORT = "IMPORT"
    ASSIGN = "ASSIGN"
    REVOKE = "REVOKE"


class ResourceType(str, Enum):
    """Tipos de recursos do sistema"""
    USER = "USER"
    ROLE = "ROLE"
    PERMISSION = "PERMISSION"
    CITIZEN = "CITIZEN"
    BIRTH = "BIRTH"
    DEATH = "DEATH"
    MARRIAGE = "MARRIAGE"
    CERTIFICATE = "CERTIFICATE"
    AUDIT = "AUDIT"
    SESSION = "SESSION"
    SYSTEM = "SYSTEM"


class AuditAction(str, Enum):
    """Ações de auditoria"""
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    LOGIN_FAILED = "LOGIN_FAILED"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    VIEW = "VIEW"
    EXPORT = "EXPORT"
    ASSIGN = "ASSIGN"
    REVOKE = "REVOKE"
    PASSWORD_CHANGE = "PASSWORD_CHANGE"
    PASSWORD_RESET = "PASSWORD_RESET"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class MFAType(str, Enum):
    """Tipos de MFA suportados"""
    NONE = "NONE"
    EMAIL = "EMAIL"
    SMS = "SMS"
    TOTP = "TOTP"
    BIOMETRIC = "BIOMETRIC"
