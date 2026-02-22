from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import uuid4

from ..enums.user_status import AuditAction, ResourceType


@dataclass
class AuditLog:
    """Log de auditoria (imutável)"""
    id: str = field(default_factory=lambda: str(uuid4()))
    user_id: Optional[str] = None
    username: Optional[str] = None
    
    # Ação
    action: AuditAction = field(default=None)
    resource: ResourceType = field(default=None)
    resource_id: Optional[str] = None
    
    # Detalhes
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)
    
    # Resultado
    success: bool = True
    error_message: Optional[str] = None
    
    # Timestamp
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Garante imutabilidade básica"""
        if not self.action or not self.resource:
            raise ValueError("Action e resource são obrigatórios")
    
    @classmethod
    def create(cls, action: AuditAction, resource: ResourceType, 
               user_id: Optional[str] = None, **kwargs) -> 'AuditLog':
        """Factory method para criar log"""
        return cls(
            action=action,
            resource=resource,
            user_id=user_id,
            **kwargs
        )
    
    @classmethod
    def login_success(cls, user_id: str, username: str, ip: Optional[str] = None, 
                      agent: Optional[str] = None) -> 'AuditLog':
        """Log de login bem-sucedido"""
        return cls(
            user_id=user_id,
            username=username,
            action=AuditAction.LOGIN,
            resource=ResourceType.SESSION,
            ip_address=ip,
            user_agent=agent,
            success=True
        )
    
    @classmethod
    def login_failed(cls, username: str, ip: Optional[str] = None, 
                     reason: str = "invalid_credentials") -> 'AuditLog':
        """Log de login falho"""
        return cls(
            username=username,
            action=AuditAction.LOGIN_FAILED,
            resource=ResourceType.SESSION,
            ip_address=ip,
            success=False,
            details={"reason": reason}
        )
    
    @classmethod
    def permission_denied(cls, user_id: str, resource: str, action: str,
                          ip: Optional[str] = None) -> 'AuditLog':
        """Log de permissão negada"""
        return cls(
            user_id=user_id,
            action=AuditAction.PERMISSION_DENIED,
            resource=ResourceType.SYSTEM,
            ip_address=ip,
            success=False,
            details={"required_resource": resource, "required_action": action}
        )
    
    @classmethod
    def data_change(cls, user_id: str, resource: ResourceType, resource_id: str,
                    action: AuditAction, old_values: dict, new_values: dict,
                    ip: Optional[str] = None) -> 'AuditLog':
        """Log de alteração de dados"""
        return cls(
            user_id=user_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            ip_address=ip,
            details={
                "old": old_values,
                "new": new_values,
                "changed_fields": list(set(old_values.keys()) & set(new_values.keys()))
            }
        )
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "username": self.username,
            "action": self.action.value,
            "resource": self.resource.value,
            "resource_id": self.resource_id,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "success": self.success,
            "error_message": self.error_message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat()
        }
