"""Status enumerations for domain entities"""
from enum import Enum
from typing import List

class EntityStatus(str, Enum):
    """
    Base entity status enumeration.
    
    Represents standard lifecycle states for most domain entities.
    """
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    ARCHIVED = 'archived'

    @classmethod
    def all_values(cls) -> List[str]:
        """Get all status values"""
        return [status.value for status in cls]

    @classmethod
    def is_valid(cls, value: str) -> bool:
        """Check if value is valid status"""
        return value in cls.all_values()

class ProcessStatus(str, Enum):
    """
    Process execution status enumeration.
    
    Represents states during process/workflow execution.
    """
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'

    def is_completed(self) -> bool:
        """Check if process is in terminal state"""
        return self in (self.COMPLETED, self.FAILED, self.CANCELLED)

    def is_active(self) -> bool:
        """Check if process is active"""
        return self in (self.PENDING, self.IN_PROGRESS)

    @classmethod
    def all_values(cls) -> List[str]:
        """Get all status values"""
        return [status.value for status in cls]

class LifecycleStatus(str, Enum):
    """
    Entity lifecycle status enumeration.
    
    Represents progression through entity lifecycle stages.
    """
    DRAFT = 'draft'
    SUBMITTED = 'submitted'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    PUBLISHED = 'published'
    EXPIRED = 'expired'

class AuditStatus(str, Enum):
    """
    Audit/compliance status enumeration.
    
    Represents audit and compliance states.
    """
    PENDING_AUDIT = 'pending_audit'
    AUDITED = 'audited'
    COMPLIANT = 'compliant'
    NON_COMPLIANT = 'non_compliant'
    AWAITING_REMEDIATION = 'awaiting_remediation'
__all__ = ['EntityStatus', 'ProcessStatus', 'LifecycleStatus', 'AuditStatus']