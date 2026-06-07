"""
TEMPLATE: Domain Exception Consolidation (Phase 1 - P0-B Integration)

This template shows how 26 domain_exception.py files
should be refactored to use DomainExceptionFactory.

Replace the content of:
  apps/backend/app/modules/{module_name}/domain/exceptions/domain_exception.py

With this pattern:
"""

# ============================================================================
# EXAMPLE: apps/backend/app/modules/documents/domain/exceptions/domain_exception.py
# ============================================================================

"""Domain base exception for module"""
# Re-export core implementation
from apps.backend.core.exceptions.domain_exception import DomainException

__all__ = ["DomainException"]

# ============================================================================
# HOW IT WORKS (P0-B Integration):
# ============================================================================
#
# 1. Each module's domain/exceptions/domain_exception.py simply re-exports
#    the core DomainException
#
# 2. Eliminates 26 phantom files by pointing to single source of truth
#
# 3. Keep backwards compatibility:
#    - Code importing from module still works:
#      from apps.backend.app.modules.documents.domain.exceptions import DomainException
#
# 4. Result: 26 files become 1 line each → easy to delete later
#
# ============================================================================
