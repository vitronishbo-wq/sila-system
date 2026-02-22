"""
Service Hub Schemas

Schemas de validação para o catálogo de serviços públicos digitais.
"""

from .service_hub import (
    ServiceBase,
    ServiceCreate,
    ServiceLocationBase,
    ServiceLocationCreate,
    ServiceLocationRead,
    ServiceLocationUpdate,
    ServiceRead,
    ServiceUpdate,
    ServiceWithLocations,
    ServiceFilters,
    ServiceLocationFilters,
)

from .service_registry import (
    ServiceRegistryBase,
    ServiceRegistryCreate,
    ServiceRegistryUpdate,
    ServiceRegistryRead,
)

__all__ = [
    # Service Hub
    "ServiceBase",
    "ServiceCreate",
    "ServiceUpdate",
    "ServiceRead",
    "ServiceLocationBase",
    "ServiceLocationCreate",
    "ServiceLocationUpdate",
    "ServiceLocationRead",
    "ServiceWithLocations",
    "ServiceFilters",
    "ServiceLocationFilters",
    # Service Registry
    "ServiceRegistryBase",
    "ServiceRegistryCreate",
    "ServiceRegistryUpdate",
    "ServiceRegistryRead",
]
