"""Central audit engine for SILA system"""
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from abc import ABC, abstractmethod
from uuid import uuid4

class AuditAction(str, Enum):
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    APPROVE = "APPROVE"
    LOGIN = "LOGIN"

class AuditStatus(str, Enum):
    INITIATED = "INITIATED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class AuditSeverity(str, Enum):
    INFO = "INFO"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

@dataclass
class AuditRecord:
    audit_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    user_id: str = ""
    module: str = ""
    action: AuditAction = AuditAction.READ
    status: AuditStatus = AuditStatus.INITIATED
    request_path: str = ""
    result_code: int = 0
    result_message: str = ""

class AuditAdapter(ABC):
    async def store(self, record: AuditRecord) -> bool: pass
    async def retrieve(self, audit_id: str) -> Optional[AuditRecord]: pass
    async def query(self, **filters) -> List[AuditRecord]: pass

class InMemoryAuditAdapter(AuditAdapter):
    def __init__(self):
        self.records: Dict[str, AuditRecord] = {}
    async def store(self, record: AuditRecord) -> bool:
        self.records[record.audit_id] = record
        return True
    async def retrieve(self, audit_id: str) -> Optional[AuditRecord]:
        return self.records.get(audit_id)
    async def query(self, **filters) -> List[AuditRecord]:
        return list(self.records.values())

class AuditEngine:
    def __init__(self, adapter: Optional[AuditAdapter] = None):
        self.adapter = adapter or InMemoryAuditAdapter()
        self._pending = {}
    
    async def initiate(self, user_id: str, module: str, action: AuditAction,
                      request_path: str = "", request_method: str = "GET") -> AuditRecord:
        record = AuditRecord(user_id=user_id, module=module, action=action,
                           request_path=request_path)
        self._pending[record.audit_id] = record
        return record
    
    async def complete(self, audit_id: str, result_code: int = 200) -> bool:
        if audit_id not in self._pending:
            return False
        record = self._pending[audit_id]
        record.status = AuditStatus.COMPLETED
        record.result_code = result_code
        await self.adapter.store(record)
        del self._pending[audit_id]
        return True
    
    async def fail(self, audit_id: str, error_code: int = 500, error_message: str = "") -> bool:
        if audit_id not in self._pending:
            return False
        record = self._pending[audit_id]
        record.status = AuditStatus.FAILED
        record.result_code = error_code
        record.result_message = error_message
        await self.adapter.store(record)
        del self._pending[audit_id]
        return True

_audit_engine: Optional[AuditEngine] = None

def get_audit_engine() -> AuditEngine:
    global _audit_engine
    if _audit_engine is None:
        _audit_engine = AuditEngine()
    return _audit_engine

async def initialize_audit(adapter: Optional[AuditAdapter] = None) -> AuditEngine:
    global _audit_engine
    _audit_engine = AuditEngine(adapter)
    return _audit_engine
