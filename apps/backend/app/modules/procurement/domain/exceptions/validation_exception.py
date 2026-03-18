"""Domain validation exceptions"""
from typing import List, Dict, Any, Optional
from apps.backend.core.exceptions.domain_exception import DomainException

class ValidationException(DomainException):
    """
    Base exception for domain validation failures.
    
    Used when entity violates domain rules or invariants.
    """

    def __init__(self, message: str, violations: Optional[List[str]]=None):
        """
        Initialize validation exception.
        
        Args:
            message: Main validation error message
            violations: List of specific violations
        """
        self.violations = violations or []
        context = {}
        if self.violations:
            context['violations'] = self.violations
        super().__init__(message=message, code='VALIDATION_ERROR', context=context)

class InvalidEntityException(ValidationException):
    """
    Raised when entity violates domain invariants.
    
    Used for:
    - Invalid state transitions
    - Business rule violations
    - Constraint violations
    """

    def __init__(self, entity_type: str, violations: List[str]):
        """
        Initialize invalid entity exception.
        
        Args:
            entity_type: Type of invalid entity
            violations: List of invariant violations
        """
        message = f'{entity_type} violates domain invariants'
        super().__init__(message=message, violations=violations)
        self.code = 'INVALID_ENTITY'
        self.context['entity_type'] = entity_type

class BusinessRuleException(ValidationException):
    """
    Raised when business logic rule is violated.
    
    Used for:
    - Insufficient balance for transaction
    - Duplicate unique values
    - State machine violations
    """

    def __init__(self, rule: str, message: str, details: Optional[Dict[str, Any]]=None):
        """
        Initialize business rule exception.
        
        Args:
            rule: Name of violated business rule
            message: Description of violation
            details: Additional details about violation
        """
        super().__init__(message=message)
        self.code = 'BUSINESS_RULE_VIOLATED'
        self.context = {'rule': rule, **(details or {})}

class ValueObjectCreationException(ValidationException):
    """
    Raised when value object creation fails.
    
    Used for:
    - Invalid constructor parameters
    - Type mismatches
    - Range violations
    """

    def __init__(self, value_object_type: str, message: str, violations: Optional[List[str]]=None):
        """
        Initialize value object creation exception.
        
        Args:
            value_object_type: Type of value object
            message: Description of failure
            violations: List of specific violations
        """
        super().__init__(message=message, violations=violations)
        self.code = 'INVALID_VALUE_OBJECT'
        self.context['value_object_type'] = value_object_type
__all__ = ['ValidationException', 'InvalidEntityException', 'BusinessRuleException', 'ValueObjectCreationException']