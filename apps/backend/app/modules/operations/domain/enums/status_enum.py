"""Status enumerations for domain entities"""

from enum import StrEnum


class EntityStatus(StrEnum):
    """
    Base entity status enumeration.

    Represents standard lifecycle states for most domain entities.
    """

    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"

    @classmethod
    def all_values(cls) -> list[str]:
        """Get all status values"""
        return [status.value for status in cls]

    @classmethod
    def is_valid(cls, value: str) -> bool:
        """Check if value is valid status"""
        return value in cls.all_values()


class ProcessStatus(StrEnum):
    """
    Process execution status enumeration.

    Represents states during process/workflow execution.
    """

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

    def is_completed(self) -> bool:
        """Check if process is in terminal state"""
        return self in (self.COMPLETED, self.FAILED, self.CANCELLED)

    def is_active(self) -> bool:
        """Check if process is active"""
        return self in (self.PENDING, self.IN_PROGRESS)

    @classmethod
    def all_values(cls) -> list[str]:
        """Get all status values"""
        return [status.value for status in cls]


class LifecycleStatus(StrEnum):
    """
    Entity lifecycle status enumeration.

    Represents progression through entity lifecycle stages.
    """

    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"
    EXPIRED = "expired"


class AuditStatus(StrEnum):
    """
    Audit/compliance status enumeration.

    Represents audit and compliance states.
    """

    PENDING_AUDIT = "pending_audit"
    AUDITED = "audited"
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    AWAITING_REMEDIATION = "awaiting_remediation"


class OrderStatus(StrEnum):
    """
    Order lifecycle status used by operations workflows.
    """

    DRAFT = "draft"
    SUBMITTED = "submitted"
    IN_REVIEW = "in_review"
    AWAITING_PAYMENT = "awaiting_payment"
    PAID = "paid"
    COMPLETED = "completed"
    REJECTED = "rejected"


class PaymentStatus(StrEnum):
    """
    Payment status used by operations workflows.
    """

    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"


__all__ = [
    "EntityStatus",
    "ProcessStatus",
    "LifecycleStatus",
    "AuditStatus",
    "OrderStatus",
    "PaymentStatus",
]
