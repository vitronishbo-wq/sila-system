"""
RBAC (Role-Based Access Control) do SILA

Implementa:
- Controle territorial hierárquico (closure table)
- Verificação de permissões por role + territory
- Dependencies para FastAPI endpoints
"""

from .territorial_access import (
    verify_territorial_access,
    verify_same_territory_or_child,
    require_territorial_access,
    require_admin,
    require_not_citizen,
    TerritorialAccessDenied,
)

__all__ = [
    "verify_territorial_access",
    "verify_same_territory_or_child",
    "require_territorial_access",
    "require_admin",
    "require_not_citizen",
    "TerritorialAccessDenied",
]
