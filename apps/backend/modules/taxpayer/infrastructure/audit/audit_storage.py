"""Audit Storage and Persistence"""

from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
from .audit_logger import AuditEntry, AuditAction, AuditLevel
from datetime import datetime, timedelta


class AuditStorage(ABC):
    """Abstract audit storage interface"""
    
    @abstractmethod
    async def store(self, entry: AuditEntry) -> str:
        """Store audit entry"""
        pass
    
    @abstractmethod
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
        pass


class InMemoryAuditStorage(AuditStorage):
    """In-memory audit storage for testing"""
    
    def __init__(self, max_entries: int = 10000):
        self._entries: Dict[str, AuditEntry] = {}
        self._max_entries = max_entries
    
    async def store(self, entry: AuditEntry) -> str:
        """Store audit entry in memory"""
        if len(self._entries) >= self._max_entries:
            # Remove oldest entry
            oldest_key = min(self._entries.keys(), key=lambda k: self._entries[k].timestamp)
            del self._entries[oldest_key]
        
        self._entries[entry.id] = entry
        return entry.id
    
    async def search(
        self,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        user_id: Optional[str] = None,
        action: Optional[AuditAction] = None,
        level: Optional[AuditLevel] = None,
        limit: int = 100,
    ) -> List[AuditEntry]:
        """Search entries in memory"""
        results = list(self._entries.values())
        
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
        
        # Sort by timestamp descending and limit
        results.sort(key=lambda e: e.timestamp, reverse=True)
        return results[:limit]
    
    def get_all(self) -> List[AuditEntry]:
        """Get all entries"""
        return sorted(self._entries.values(), key=lambda e: e.timestamp, reverse=True)
    
    def clear(self) -> int:
        """Clear all entries"""
        count = len(self._entries)
        self._entries.clear()
        return count


class DatabaseAuditStorage(AuditStorage):
    """Database-backed audit storage"""
    
    def __init__(self, db_session):
        self.db = db_session  # SQLAlchemy AsyncSession
    
    async def store(self, entry: AuditEntry) -> str:
        """Store audit entry in database"""
        from ..db.models import TaxAuditModel
        
        db_entry = TaxAuditModel(
            action=entry.action.value,
            entity_type=entry.entity_type,
            entity_id=entry.entity_id,
            user_id=entry.user_id,
            description=entry.description,
            level=entry.level.value,
            old_values=entry.old_values,
            new_values=entry.new_values,
            details=entry.metadata,
            ip_address=entry.ip_address,
            user_agent=entry.user_agent,
        )
        
        self.db.add(db_entry)
        await self.db.commit()
        await self.db.refresh(db_entry)
        
        return str(db_entry.id)
    
    async def search(
        self,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        user_id: Optional[str] = None,
        action: Optional[AuditAction] = None,
        level: Optional[AuditLevel] = None,
        limit: int = 100,
    ) -> List[AuditEntry]:
        """Search entries in database"""
        from sqlalchemy import select, desc
        from ..db.models import TaxAuditModel
        
        query = select(TaxAuditModel)
        
        if entity_type:
            query = query.where(TaxAuditModel.entity_type == entity_type)
        if entity_id:
            query = query.where(TaxAuditModel.entity_id == entity_id)
        if user_id:
            query = query.where(TaxAuditModel.user_id == user_id)
        if action:
            query = query.where(TaxAuditModel.action == action.value)
        if level:
            query = query.where(TaxAuditModel.level == level.value)
        
        query = query.order_by(desc(TaxAuditModel.created_at)).limit(limit)
        
        result = await self.db.execute(query)
        entries = result.scalars().all()
        
        # Convert to AuditEntry objects
        return [self._to_audit_entry(e) for e in entries]
    
    @staticmethod
    def _to_audit_entry(db_entry) -> AuditEntry:
        """Convert database entry to AuditEntry"""
        return AuditEntry(
            action=AuditAction[db_entry.action],
            entity_type=db_entry.entity_type,
            entity_id=db_entry.entity_id,
            user_id=db_entry.user_id,
            description=db_entry.description,
            level=AuditLevel[db_entry.level] if db_entry.level else AuditLevel.INFO,
            old_values=db_entry.old_values,
            new_values=db_entry.new_values,
            metadata=db_entry.details,
            ip_address=db_entry.ip_address,
            user_agent=db_entry.user_agent,
        )


class FileAuditStorage(AuditStorage):
    """File-based audit storage (CSV/JSON)"""
    
    def __init__(self, file_path: str, format: str = "json"):
        self.file_path = file_path
        self.format = format  # "json" or "csv"
        self._entries: List[AuditEntry] = []
    
    async def store(self, entry: AuditEntry) -> str:
        """Store entry and append to file"""
        import json
        from pathlib import Path
        
        self._entries.append(entry)
        
        # Append to file
        path = Path(self.file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'a') as f:
            f.write(json.dumps(entry.to_dict()) + '\n')
        
        return entry.id
    
    async def search(
        self,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        user_id: Optional[str] = None,
        action: Optional[AuditAction] = None,
        level: Optional[AuditLevel] = None,
        limit: int = 100,
    ) -> List[AuditEntry]:
        """Search entries in file"""
        await self._load_entries()
        
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
        
        results.sort(key=lambda e: e.timestamp, reverse=True)
        return results[:limit]
    
    async def _load_entries(self):
        """Load entries from file"""
        import json
        from pathlib import Path
        
        path = Path(self.file_path)
        if not path.exists():
            return
        
        self._entries.clear()
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        data = json.loads(line)
                        entry = self._dict_to_entry(data)
                        self._entries.append(entry)
                    except json.JSONDecodeError:
                        continue
    
    @staticmethod
    def _dict_to_entry(data: Dict) -> AuditEntry:
        """Convert dict to AuditEntry"""
        return AuditEntry(
            action=AuditAction[data['action']],
            entity_type=data['entity_type'],
            entity_id=data['entity_id'],
            user_id=data['user_id'],
            description=data['description'],
            level=AuditLevel[data.get('level', 'INFO')],
            old_values=data.get('old_values', {}),
            new_values=data.get('new_values', {}),
            metadata=data.get('metadata', {}),
            ip_address=data.get('ip_address'),
            user_agent=data.get('user_agent'),
        )
