#!/bin/bash
# SILA System - Domain Exceptions Framework
# Objetivo: Criar exceções padrão em todos módulos (+25 arquivos)
# Generated: 2026-03-14

set -e

MODULES_DIR="apps/backend/app/modules"
TOTAL_MODULES=0
MODULES_CREATED=0
FILES_CREATED=0

echo "🚨 [Domain Exceptions] Starting standardized exception framework..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Create exceptions file structure in each module
create_domain_exceptions() {
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
    
    # Create exceptions directory
    local exceptions_dir="$module_dir/domain/exceptions"
    mkdir -p "$exceptions_dir"
    
    # Create domain_exception.py (base class)
    if [ ! -f "$exceptions_dir/domain_exception.py" ]; then
        cat > "$exceptions_dir/domain_exception.py" << 'DOMAIN_EXC'
"""Base domain exception class"""
from typing import Optional, Dict, Any


class DomainException(Exception):
    """
    Base exception for all domain-level errors.
    
    Provides standardized error tracking and context information.
    """
    
    def __init__(
        self,
        message: str,
        code: str = "DOMAIN_ERROR",
        context: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize domain exception.
        
        Args:
            message: Human-readable error message
            code: Machine-readable error code
            context: Additional context information
        """
        self.message = message
        self.code = code
        self.context = context or {}
        
        # Format full message with code
        full_message = f"[{code}] {message}"
        if self.context:
            full_message += f" | Context: {self.context}"
        
        super().__init__(full_message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for logging/API responses"""
        return {
            "error": self.__class__.__name__,
            "code": self.code,
            "message": self.message,
            "context": self.context,
        }


__all__ = ["DomainException"]
DOMAIN_EXC
        
        FILES_CREATED=$((FILES_CREATED + 1))
    fi
    
    # Create not_found_exception.py
    if [ ! -f "$exceptions_dir/not_found_exception.py" ]; then
        cat > "$exceptions_dir/not_found_exception.py" << 'NOT_FOUND_EXC'
"""Entity not found exception"""
from typing import Any
from .domain_exception import DomainException


class EntityNotFoundException(DomainException):
    """
    Raised when an entity is not found in repository.
    
    Used for:
    - Repository queries returning no results
    - Lookup failures by ID or unique fields
    - Aggregates not found in store
    """
    
    def __init__(self, entity_type: str, entity_id: Any):
        """
        Initialize entity not found exception.
        
        Args:
            entity_type: Name of entity type (e.g., "User", "Order")
            entity_id: ID or identifier of missing entity
        """
        message = f"{entity_type} with ID '{entity_id}' not found"
        super().__init__(
            message=message,
            code="ENTITY_NOT_FOUND",
            context={
                "entity_type": entity_type,
                "entity_id": str(entity_id),
            }
        )


class AggregateNotFoundException(DomainException):
    """
    Raised when an aggregate root is not found.
    
    Specialization of EntityNotFoundException for aggregate roots.
    """
    
    def __init__(self, aggregate_type: str, aggregate_id: Any):
        """
        Initialize aggregate not found exception.
        
        Args:
            aggregate_type: Name of aggregate root (e.g., "Order", "Customer")
            aggregate_id: ID of missing aggregate
        """
        message = f"Aggregate {aggregate_type} with ID '{aggregate_id}' not found"
        super().__init__(
            message=message,
            code="AGGREGATE_NOT_FOUND",
            context={
                "aggregate_type": aggregate_type,
                "aggregate_id": str(aggregate_id),
            }
        )


__all__ = ["EntityNotFoundException", "AggregateNotFoundException"]
NOT_FOUND_EXC
        
        FILES_CREATED=$((FILES_CREATED + 1))
    fi
    
    # Create validation_exception.py
    if [ ! -f "$exceptions_dir/validation_exception.py" ]; then
        cat > "$exceptions_dir/validation_exception.py" << 'VALIDATION_EXC'
"""Domain validation exceptions"""
from typing import List, Dict, Any, Optional
from .domain_exception import DomainException


class ValidationException(DomainException):
    """
    Base exception for domain validation failures.
    
    Used when entity violates domain rules or invariants.
    """
    
    def __init__(
        self,
        message: str,
        violations: Optional[List[str]] = None
    ):
        """
        Initialize validation exception.
        
        Args:
            message: Main validation error message
            violations: List of specific violations
        """
        self.violations = violations or []
        
        context = {}
        if self.violations:
            context["violations"] = self.violations
        
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            context=context
        )


class InvalidEntityException(ValidationException):
    """
    Raised when entity violates domain invariants.
    
    Used for:
    - Invalid state transitions
    - Business rule violations
    - Constraint violations
    """
    
    def __init__(
        self,
        entity_type: str,
        violations: List[str]
    ):
        """
        Initialize invalid entity exception.
        
        Args:
            entity_type: Type of invalid entity
            violations: List of invariant violations
        """
        message = f"{entity_type} violates domain invariants"
        super().__init__(message=message, violations=violations)
        self.code = "INVALID_ENTITY"
        self.context["entity_type"] = entity_type


class BusinessRuleException(ValidationException):
    """
    Raised when business logic rule is violated.
    
    Used for:
    - Insufficient balance for transaction
    - Duplicate unique values
    - State machine violations
    """
    
    def __init__(
        self,
        rule: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize business rule exception.
        
        Args:
            rule: Name of violated business rule
            message: Description of violation
            details: Additional details about violation
        """
        super().__init__(message=message)
        self.code = "BUSINESS_RULE_VIOLATED"
        self.context = {
            "rule": rule,
            **(details or {})
        }


class ValueObjectCreationException(ValidationException):
    """
    Raised when value object creation fails.
    
    Used for:
    - Invalid constructor parameters
    - Type mismatches
    - Range violations
    """
    
    def __init__(
        self,
        value_object_type: str,
        message: str,
        violations: Optional[List[str]] = None
    ):
        """
        Initialize value object creation exception.
        
        Args:
            value_object_type: Type of value object
            message: Description of failure
            violations: List of specific violations
        """
        super().__init__(message=message, violations=violations)
        self.code = "INVALID_VALUE_OBJECT"
        self.context["value_object_type"] = value_object_type


__all__ = [
    "ValidationException",
    "InvalidEntityException",
    "BusinessRuleException",
    "ValueObjectCreationException",
]
VALIDATION_EXC
        
        FILES_CREATED=$((FILES_CREATED + 1))
    fi
    
    # Create __init__.py in exceptions directory
    if [ ! -f "$exceptions_dir/__init__.py" ]; then
        cat > "$exceptions_dir/__init__.py" << 'EXCEPTIONS_INIT'
"""Domain exceptions module"""
from .domain_exception import DomainException
from .not_found_exception import (
    EntityNotFoundException,
    AggregateNotFoundException,
)
from .validation_exception import (
    ValidationException,
    InvalidEntityException,
    BusinessRuleException,
    ValueObjectCreationException,
)

__all__ = [
    "DomainException",
    "EntityNotFoundException",
    "AggregateNotFoundException",
    "ValidationException",
    "InvalidEntityException",
    "BusinessRuleException",
    "ValueObjectCreationException",
]
EXCEPTIONS_INIT
        
        FILES_CREATED=$((FILES_CREATED + 1))
    fi
    
    MODULES_CREATED=$((MODULES_CREATED + 1))
    echo "✓ $module_name"
}

# Process all modules
echo "📦 Creating domain exceptions..."
echo ""

for module_dir in "$MODULES_DIR"/*; do
    if [ -d "$module_dir" ]; then
        create_domain_exceptions "$module_dir" || true
    fi
done

# Summary
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ DOMAIN EXCEPTIONS FRAMEWORK COMPLETE"
echo "═══════════════════════════════════════════════════════════════"
echo "📊 Summary:"
echo "   • Modules processed: $TOTAL_MODULES"
echo "   • Modules with exceptions: $MODULES_CREATED"
echo "   • Files created: $FILES_CREATED"
echo ""
echo "📁 Structure per module:"
echo "   domain/exceptions/"
echo "   ├── __init__.py"
echo "   ├── domain_exception.py (base)"
echo "   ├── not_found_exception.py"
echo "   └── validation_exception.py"
echo ""
echo "🚀 Exception Hierarchy:"
echo "   DomainException"
echo "   ├── EntityNotFoundException"
echo "   ├── AggregateNotFoundException"
echo "   └── ValidationException"
echo "       ├── InvalidEntityException"
echo "       ├── BusinessRuleException"
echo "       └── ValueObjectCreationException"
echo ""
echo "═══════════════════════════════════════════════════════════════"
