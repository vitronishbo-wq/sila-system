from enum import StrEnum


class WorkflowStatus(StrEnum):
    ACTIVE = "active"
    COMPLETED = "completed"
    TERMINATED = "terminated"
    SUSPENDED = "suspended"
    EXPIRED = "expired"


class TaskStatus(StrEnum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class TaskPriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


class TransitionType(StrEnum):
    AUTOMATIC = "automatic"
    USER = "user"
    SYSTEM = "system"
    SCHEDULED = "scheduled"
    CONDITIONAL = "conditional"


class AssignmentType(StrEnum):
    ROLE = "role"
    USER = "user"
    GROUP = "group"
    POOL = "pool"
    EXPRESSION = "expression"


class EntityType(StrEnum):
    SERVICE_REQUEST = "service_request"
    CITIZEN = "citizen"
    DOCUMENT = "document"
    PAYMENT = "payment"
    LICENSE = "license"
    PROCESS = "process"
