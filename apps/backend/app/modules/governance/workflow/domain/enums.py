from enum import Enum

class WorkflowStatus(str, Enum):
    ACTIVE = 'active'
    COMPLETED = 'completed'
    TERMINATED = 'terminated'
    SUSPENDED = 'suspended'
    EXPIRED = 'expired'

class TaskStatus(str, Enum):
    PENDING = 'pending'
    ASSIGNED = 'assigned'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    SKIPPED = 'skipped'
    CANCELLED = 'cancelled'
    EXPIRED = 'expired'

class TaskPriority(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    URGENT = 'urgent'
    CRITICAL = 'critical'

class TransitionType(str, Enum):
    AUTOMATIC = 'automatic'
    USER = 'user'
    SYSTEM = 'system'
    SCHEDULED = 'scheduled'
    CONDITIONAL = 'conditional'

class AssignmentType(str, Enum):
    ROLE = 'role'
    USER = 'user'
    GROUP = 'group'
    POOL = 'pool'
    EXPRESSION = 'expression'

class EntityType(str, Enum):
    SERVICE_REQUEST = 'service_request'
    CITIZEN = 'citizen'
    DOCUMENT = 'document'
    PAYMENT = 'payment'
    LICENSE = 'license'
    PROCESS = 'process'