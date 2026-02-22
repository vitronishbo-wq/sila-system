"""Structured Audit Logger"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum
import json


class AuditAction(str, Enum):
    """Audit action types"""
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    SUBMIT = "SUBMIT"
    EXPORT = "EXPORT"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    FAILED_LOGIN = "FAILED_LOGIN"


class AuditLevel(str, Enum):
    """Audit severity level"""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class AuditEntry:
    """Audit log entry"""
    
    def __init__(
        self,
        action: AuditAction,
        entity_type: str,
        entity_id: str,
        user_id: str,
        description: str,
        level: AuditLevel = AuditLevel.INFO,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ):
        self.id = f"{action.value}_{entity_type}_{entity_id}_{datetime.now().timestamp()}"
        self.action = action
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.user_id = user_id
        self.description = description
        self.level = level
        self.old_values = old_values or {}
        self.new_values = new_values or {}
        self.metadata = metadata or {}
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'action': self.action.value,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'user_id': self.user_id,
            'description': self.description,
            'level': self.level.value,
            'old_values': self.old_values,
            'new_values': self.new_values,
            'metadata': self.metadata,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'timestamp': self.timestamp.isoformat(),
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict())


class AuditLogger:
    """Central audit logging service"""
    
    def __init__(self, storage=None):
        self.storage = storage  # AbstractAuditStorage
        self._entries: List[AuditEntry] = []
    
    async def log(
        self,
        action: AuditAction,
        entity_type: str,
        entity_id: str,
        user_id: str,
        description: str,
        level: AuditLevel = AuditLevel.INFO,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AuditEntry:
        """Log audit entry"""
        entry = AuditEntry(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            user_id=user_id,
            description=description,
            level=level,
            old_values=old_values,
            new_values=new_values,
            metadata=metadata,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        
        # Store locally
        self._entries.append(entry)
        
        # Persist to storage if available
        if self.storage:
            await self.storage.store(entry)
        
        return entry
    
    async def log_creation(
        self,
        entity_type: str,
        entity_id: str,
        user_id: str,
        new_values: Dict[str, Any],
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AuditEntry:
        """Log entity creation"""
        return await self.log(
            action=AuditAction.CREATE,
            entity_type=entity_type,
            entity_id=entity_id,
            user_id=user_id,
            description=f"Created {entity_type}",
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent,
        )
    
    async def log_update(
        self,
        entity_type: str,
        entity_id: str,
        user_id: str,
        old_values: Dict[str, Any],
        new_values: Dict[str, Any],
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AuditEntry:
        """Log entity update"""
        return await self.log(
            action=AuditAction.UPDATE,
            entity_type=entity_type,
            entity_id=entity_id,
            user_id=user_id,
            description=f"Updated {entity_type}",
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent,
        )
    
    async def log_deletion(
        self,
        entity_type: str,
        entity_id: str,
        user_id: str,
        old_values: Dict[str, Any],
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AuditEntry:
        """Log entity deletion"""
        return await self.log(
            action=AuditAction.DELETE,
            entity_type=entity_type,
            entity_id=entity_id,
            user_id=user_id,
            description=f"Deleted {entity_type}",
            old_values=old_values,
            ip_address=ip_address,
            user_agent=user_agent,
        )
    
    async def log_approval(
        self,
        entity_type: str,
        entity_id: str,
        user_id: str,
        reason: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AuditEntry:
        """Log approval action"""
        return await self.log(
            action=AuditAction.APPROVE,
            entity_type=entity_type,
            entity_id=entity_id,
            user_id=user_id,
            description=f"Approved {entity_type}: {reason}",
            ip_address=ip_address,
            user_agent=user_agent,
        )
    
    async def log_rejection(
        self,
        entity_type: str,
        entity_id: str,
        user_id: str,
        reason: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AuditEntry:
        """Log rejection action"""
        return await self.log(
            action=AuditAction.REJECT,
            entity_type=entity_type,
            entity_id=entity_id,
            user_id=user_id,
            description=f"Rejected {entity_type}: {reason}",
            level=AuditLevel.WARNING,
            ip_address=ip_address,
            user_agent=user_agent,
        )
    
    def get_local_entries(self, limit: int = 100) -> List[AuditEntry]:
        """Get recent local entries"""
        return self._entries[-limit:]
    
    async def search(
        self,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        user_id: Optional[str] = None,
        action: Optional[AuditAction] = None,
        level: Optional[AuditLevel] = None,
        limit: int = 100,
    ) -> List[AuditEntry]:
        """Search audit entries"""
        if self.storage:
            return await self.storage.search(
                entity_type=entity_type,
                entity_id=entity_id,
                user_id=user_id,
                action=action,
                level=level,
                limit=limit,
            )
        else:
            # Search local entries
            results = self._entries
            
            if entity_type:
                results = [e for e in results if e.entity_type == entity_type]
            if entity_id:
                results = [e for e in results if e.entity_id == entity_id]
            if user_id:
                results = [e for e in results if e.user_id == user_id]
            if action:
                results = [e for e in results if e.action == action]
            if level:
                results = [e for e in results if e.level == level]
            
            return results[-limit:]
    
    def clear(self) -> int:
        """Clear local entries"""
        count = len(self._entries)
        self._entries.clear()
        return count


# Singleton instance
_logger_instance: Optional[AuditLogger] = None


def get_audit_logger(storage=None) -> AuditLogger:
    """Get audit logger instance"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = AuditLogger(storage=storage)
    return _logger_instance
