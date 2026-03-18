"""Compliance domain enums."""
from enum import Enum

class ComplianceStatus(Enum):
    """Compliance check status enumeration."""
    PENDING = 'PENDING'
    PASSED = 'PASSED'
    FAILED = 'FAILED'
    WARNING = 'WARNING'

class AuditLevel(Enum):
    """Audit log level enumeration."""
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'