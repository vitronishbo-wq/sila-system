"""
TEMPLATE: Module Exceptions Pattern (Phase 1)

This template shows how 181 module-specific exceptions.py files
should be refactored to use ModuleExceptionFactory.

Replace the content of:
  apps/backend/app/modules/{module_name}/domain/exceptions.py

With this pattern:
"""

# ============================================================================
# EXAMPLE: apps/backend/app/modules/documents/domain/exceptions.py
# ============================================================================

"""Domain exceptions for Documents module"""
from apps.backend.core.exceptions.domain_exception import DomainException
from apps.backend.core.exceptions.module_exception_factory import ModuleExceptionFactory

# Generate module-specific exceptions using factory
_exceptions = ModuleExceptionFactory.create_exceptions_with_core_base(
    module_name="Documents",
    core_domain_exception=DomainException
)

# Export exception classes
DocumentsException = _exceptions["DocumentsException"]
DocumentsNotFound = _exceptions["DocumentsNotFound"]
DocumentsValidationError = _exceptions["DocumentsValidationError"]
DocumentsInvalidStateError = _exceptions["DocumentsInvalidStateError"]

__all__ = [
    "DocumentsException",
    "DocumentsNotFound",
    "DocumentsValidationError",
    "DocumentsInvalidStateError",
]

# ============================================================================
# HOW IT WORKS:
# ============================================================================
# 
# 1. Factory generates 4 exception classes:
#    - DocumentsException (base)
#    - DocumentsNotFound (inherits from DocumentsException)
#    - DocumentsValidationError (inherits from DocumentsException)
#    - DocumentsInvalidStateError (inherits from DocumentsException)
#
# 2. All inherit from DomainException (core base)
#
# 3. Usage in module code:
#    from apps.backend.app.modules.documents.domain.exceptions import DocumentsNotFound
#    
#    if not document:
#        raise DocumentsNotFound(
#            message="Document with ID 123 not found",
#            code="DOC_NOT_FOUND"
#        )
#
# 4. Result: ONE factory replaces 181 identical hand-written exception files
#
# ============================================================================

