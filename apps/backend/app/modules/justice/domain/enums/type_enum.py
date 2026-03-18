"""Type enumerations for domain values"""
from enum import Enum
from typing import List

class EntityType(str, Enum):
    """
    Generic entity type enumeration.
    
    Used for polymorphic entity handling and type discrimination.
    """
    INDIVIDUAL = 'individual'
    ORGANIZATION = 'organization'
    SYSTEM = 'system'

class DocumentType(str, Enum):
    """
    Document type enumeration.
    
    Represents different document categories in the system.
    """
    ID = 'id'
    PASSPORT = 'passport'
    DRIVER_LICENSE = 'driver_license'
    CERTIFICATE = 'certificate'
    REGISTRATION = 'registration'
    LICENSE = 'license'
    PERMIT = 'permit'

class OperationType(str, Enum):
    """
    Database/domain operation type enumeration.
    
    Represents types of operations performed on entities.
    """
    CREATE = 'create'
    READ = 'read'
    UPDATE = 'update'
    DELETE = 'delete'
    EXPORT = 'export'
    IMPORT = 'import'

    def is_mutating(self) -> bool:
        """Check if operation mutates state"""
        return self in (self.CREATE, self.UPDATE, self.DELETE)

    def is_read_only(self) -> bool:
        """Check if operation is read-only"""
        return self in (self.READ, self.EXPORT)

class SortOrder(str, Enum):
    """
    Sort order enumeration.
    
    Used for query result ordering.
    """
    ASC = 'asc'
    DESC = 'desc'

class NotificationPriority(str, Enum):
    """
    Notification priority enumeration.
    
    Used for event and notification handling.
    """
    LOW = 'low'
    NORMAL = 'normal'
    HIGH = 'high'
    CRITICAL = 'critical'

class ValidationLevel(str, Enum):
    """
    Validation level enumeration.
    
    Represents depth of validation checks.
    """
    BASIC = 'basic'
    STANDARD = 'standard'
    STRICT = 'strict'
    COMPREHENSIVE = 'comprehensive'
__all__ = ['EntityType', 'DocumentType', 'OperationType', 'SortOrder', 'NotificationPriority', 'ValidationLevel']