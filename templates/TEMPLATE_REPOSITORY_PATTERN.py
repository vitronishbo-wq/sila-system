"""
TEMPLATE: Module Repository Pattern (Phase 1)

This template shows how 28 module-specific repositories.py files
should be refactored to use RepositoryFactory.

Replace the content of:
  apps/backend/app/modules/{module_name}/domain/repositories.py

With this pattern:
"""

# ============================================================================
# EXAMPLE: apps/backend/app/modules/documents/domain/repositories.py
# ============================================================================

"""Domain repository interfaces for Documents module"""
from abc import ABC
from apps.backend.core.repositories.repository_factory import RepositoryFactory

# Generate repository interface using factory
IDocumentsRepository = RepositoryFactory.create_repository_interface("Documents")

__all__ = ["IDocumentsRepository"]

# ============================================================================
# HOW IT WORKS:
# ============================================================================
#
# 1. Factory generates IDocumentsRepository with 5 abstract methods:
#    - async find_all() -> List[T]
#    - async find_by_id(id) -> Optional[T]
#    - async save(entity) -> T
#    - async delete(id) -> bool
#    - async exists(id) -> bool
#
# 2. Usage in infrastructure/repositories:
#    class DocumentsRepositoryImpl(IDocumentsRepository):
#        async def find_all(self):
#            # Implementation
#            pass
#        # ... other methods
#
# 3. Result: ONE factory replaces 28 identical hand-written interface files
#
# ============================================================================

