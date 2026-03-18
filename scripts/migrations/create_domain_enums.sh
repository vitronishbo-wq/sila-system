#!/bin/bash
# SILA System - Domain Enums Framework
# Objetivo: Criar enums padrão em todos módulos (+25 arquivos)
# Generated: 2026-03-14

set -e

MODULES_DIR="apps/backend/app/modules"
TOTAL_MODULES=0
MODULES_CREATED=0
FILES_CREATED=0

echo "📋 [Domain Enums] Starting standardized enum framework..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Create enums file structure in each module
create_domain_enums() {
    local module_dir="$1"
    local module_name=$(basename "$module_dir")
    
    # Skip special directories
    if [[ "$module_name" =~ ^(_|test|__pycache__) ]]; then
        return
    fi
    
    # Check if module has domain layer
    if [ ! -d "$module_dir/domain" ]; then
        return
    fi
    
    TOTAL_MODULES=$((TOTAL_MODULES + 1))
    
    # Create enums directory
    local enums_dir="$module_dir/domain/enums"
    mkdir -p "$enums_dir"
    
    # Create status_enum.py
    if [ ! -f "$enums_dir/status_enum.py" ]; then
        cat > "$enums_dir/status_enum.py" << 'STATUS_ENUM'
"""Status enumerations for domain entities"""
from enum import Enum
from typing import List


class EntityStatus(str, Enum):
    """
    Base entity status enumeration.
    
    Represents standard lifecycle states for most domain entities.
    """
    
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"
    
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
    def all_values(cls) -> List[str]:
        """Get all status values"""
        return [status.value for status in cls]


class LifecycleStatus(str, Enum):
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


class AuditStatus(str, Enum):
    """
    Audit/compliance status enumeration.
    
    Represents audit and compliance states.
    """
    
    PENDING_AUDIT = "pending_audit"
    AUDITED = "audited"
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    AWAITING_REMEDIATION = "awaiting_remediation"


__all__ = [
    "EntityStatus",
    "ProcessStatus",
    "LifecycleStatus",
    "AuditStatus",
]
STATUS_ENUM
        
        FILES_CREATED=$((FILES_CREATED + 1))
    fi
    
    # Create type_enum.py
    if [ ! -f "$enums_dir/type_enum.py" ]; then
        cat > "$enums_dir/type_enum.py" << 'TYPE_ENUM'
"""Type enumerations for domain values"""
from enum import Enum
from typing import List


class EntityType(str, Enum):
    """
    Generic entity type enumeration.
    
    Used for polymorphic entity handling and type discrimination.
    """
    
    INDIVIDUAL = "individual"
    ORGANIZATION = "organization"
    SYSTEM = "system"


class DocumentType(str, Enum):
    """
    Document type enumeration.
    
    Represents different document categories in the system.
    """
    
    ID = "id"
    PASSPORT = "passport"
    DRIVER_LICENSE = "driver_license"
    CERTIFICATE = "certificate"
    REGISTRATION = "registration"
    LICENSE = "license"
    PERMIT = "permit"


class OperationType(str, Enum):
    """
    Database/domain operation type enumeration.
    
    Represents types of operations performed on entities.
    """
    
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXPORT = "export"
    IMPORT = "import"
    
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
    
    ASC = "asc"
    DESC = "desc"


class NotificationPriority(str, Enum):
    """
    Notification priority enumeration.
    
    Used for event and notification handling.
    """
    
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class ValidationLevel(str, Enum):
    """
    Validation level enumeration.
    
    Represents depth of validation checks.
    """
    
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"
    COMPREHENSIVE = "comprehensive"


__all__ = [
    "EntityType",
    "DocumentType",
    "OperationType",
    "SortOrder",
    "NotificationPriority",
    "ValidationLevel",
]
TYPE_ENUM
        
        FILES_CREATED=$((FILES_CREATED + 1))
    fi
    
    # Create __init__.py in enums directory
    if [ ! -f "$enums_dir/__init__.py" ]; then
        cat > "$enums_dir/__init__.py" << 'ENUMS_INIT'
"""Domain enumerations module"""
from .status_enum import (
    EntityStatus,
    ProcessStatus,
    LifecycleStatus,
    AuditStatus,
)
from .type_enum import (
    EntityType,
    DocumentType,
    OperationType,
    SortOrder,
    NotificationPriority,
    ValidationLevel,
)

__all__ = [
    "EntityStatus",
    "ProcessStatus",
    "LifecycleStatus",
    "AuditStatus",
    "EntityType",
    "DocumentType",
    "OperationType",
    "SortOrder",
    "NotificationPriority",
    "ValidationLevel",
]
ENUMS_INIT
        
        FILES_CREATED=$((FILES_CREATED + 1))
    fi
    
    MODULES_CREATED=$((MODULES_CREATED + 1))
    echo "✓ $module_name"
}

# Process all modules
echo "📦 Creating domain enums..."
echo ""

for module_dir in "$MODULES_DIR"/*; do
    if [ -d "$module_dir" ]; then
        create_domain_enums "$module_dir" || true
    fi
done

# Summary
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ DOMAIN ENUMS FRAMEWORK COMPLETE"
echo "═══════════════════════════════════════════════════════════════"
echo "📊 Summary:"
echo "   • Modules processed: $TOTAL_MODULES"
echo "   • Modules with enums: $MODULES_CREATED"
echo "   • Files created: $FILES_CREATED"
echo ""
echo "📁 Structure per module:"
echo "   domain/enums/"
echo "   ├── __init__.py"
echo "   ├── status_enum.py"
echo "   └── type_enum.py"
echo ""
echo "📋 Available Enums:"
echo ""
echo "   Status Enums:"
echo "   • EntityStatus (active, inactive, archived)"
echo "   • ProcessStatus (pending, in_progress, completed, failed, cancelled)"
echo "   • LifecycleStatus (draft, submitted, approved, rejected, published, expired)"
echo "   • AuditStatus (pending_audit, audited, compliant, non_compliant)"
echo ""
echo "   Type Enums:"
echo "   • EntityType (individual, organization, system)"
echo "   • DocumentType (id, passport, driver_license, certificate, etc.)"
echo "   • OperationType (create, read, update, delete, export, import)"
echo "   • SortOrder (asc, desc)"
echo "   • NotificationPriority (low, normal, high, critical)"
echo "   • ValidationLevel (basic, standard, strict, comprehensive)"
echo ""
echo "═══════════════════════════════════════════════════════════════"
