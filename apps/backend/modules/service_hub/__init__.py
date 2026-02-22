"""
Service Hub Module

Módulo do catálogo central de serviços públicos digitais do SILA.
Este módulo gerencia todos os serviços oferecidos pelo governo,
incluindo seus locais de atendimento e metadados.

Funcionalidades principais:
- Catálogo de serviços públicos
- Gestão de locais de atendimento
- Filtros e busca de serviços
- Integração com outros módulos do sistema
- API REST completa para administração e consulta

Autor: SILA Development Team
Versão: 1.0.0
"""

"""Module initialization with path configuration."""

import sys
from pathlib import Path
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

# Ensure backend is in path for imports
_backend_path = Path(__file__).parent.parent.parent
if str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

# Import models
from .models import Service, ServiceLocation, ServiceRegistry

# Import schemas
from .schemas import (
    ServiceCreate,
    ServiceLocationCreate,
    ServiceLocationRead,
    ServiceLocationUpdate,
    ServiceRead,
    ServiceUpdate,
    ServiceWithLocations,
)

# Import services and CRUD
from .services import ServiceHubService
from .crud import (
    CRUDService,
    CRUDServiceLocation,
    CRUDServiceRegistry,
    get_service_crud,
    get_service_location_crud,
    get_service_registry_crud,
)

# NOTE: Router is NOT imported here to avoid circular imports
# Import it directly: from modules.service_hub.endpoints import router

# Re-export models, schemas and services
__all__ = [
    # Models
    "Service",
    "ServiceLocation",
    "ServiceRegistry",
    # Schemas
    "ServiceCreate",
    "ServiceUpdate",
    "ServiceRead",
    "ServiceLocationUpdate",
    "ServiceLocationRead",
    "ServiceWithLocations",
    # Services
    "ServiceHubService",
    # CRUD
    "CRUDService",
    "CRUDServiceLocation",
    "CRUDServiceRegistry",
    "get_service_crud",
    "get_service_location_crud",
    "get_service_registry_crud",
]

__version__ = "1.0.0"
__author__ = "SILA Development Team"
