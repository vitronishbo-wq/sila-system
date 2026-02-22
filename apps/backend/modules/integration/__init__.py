"""Module initialization with path configuration."""

import sys
from pathlib import Path

# Ensure backend is in path for imports
_backend_path = Path(__file__).parent.parent.parent
if str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

from fastapi import APIRouter

try:
    from .integration_gateway import integration_gateway
except Exception as e:
    integration_gateway = None

try:
    from .endpoints.router import router
except Exception as e:
    router = None

if router:
    api_router = APIRouter()
    api_router.include_router(router, tags=["integration"])
else:
    api_router = None

__all__ = ["api_router", "integration_gateway", "router"]


# Serviço: Sincronização BNA / BNA Synchronization

# Serviço: Gateway de API / API Gateway

# Serviço: Conector Externo / External Connector

# Serviço: Transformação de Dados / Data Transformation
