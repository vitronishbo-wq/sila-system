"""Repository Layer - DDD Aggregate Root Pattern

Following Domain-Driven Design principles:

✅ Repository ONLY for Aggregate Roots
- TaxpayerRepository: Handles Taxpayer + all child entities
  (Declarations, Debts, Payments, Certificates)

✅ No separate repositories for child entities
- Child entities accessed through Aggregate Root repository
- Maintains transactional consistency
- Ensures aggregate invariants

✅ BaseRepository: Generic CRUD base class
- Generic[T] for type safety
- Pagination and filtering
- Soft delete support

✅ AuditRepository: Cross-cutting concern
- System-wide audit trail
- Not part of any specific aggregate
"""

from .base_repository import BaseRepository
from .taxpayer_repository import TaxpayerRepository
from .audit_repository import AuditRepository

__all__ = [
    'BaseRepository',
    'TaxpayerRepository',
    'AuditRepository',
]

