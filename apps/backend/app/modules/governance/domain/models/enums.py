"""Governance domain enums."""
from enum import Enum

class WorkflowStatus(Enum):
    """Workflow status enumeration."""
    DRAFT = 'DRAFT'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'

class RequestStatus(Enum):
    """Governance request status enumeration."""
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    IN_REVIEW = 'IN_REVIEW'

class ApprovalLevel(Enum):
    """Approval level enumeration."""
    DEPARTMENT = 'DEPARTMENT'
    MINISTRY = 'MINISTRY'
    EXECUTIVE = 'EXECUTIVE'