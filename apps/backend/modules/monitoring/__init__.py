"""
Monitoring Module for SILA-System Backend

This module provides comprehensive monitoring, auditing, and alerting capabilities
for the SILA-System.

... (descrição do módulo omitida para brevidade)
"""

"""Module initialization with path configuration."""

import sys
from pathlib import Path

# Ensure backend is in path for imports
_backend_path = Path(__file__).parent.parent.parent
if str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

from fastapi import APIRouter
from .analytics import *
from .examples import *
from .integrations import *
from .models import *
from .schemas import *
from .security import *
from .services import *

# ----------------------------------------------------------------------
# 1. Importação e Configuração de Rotas
# ----------------------------------------------------------------------

# Router principal consolidado do módulo routes/
from .routes import router as monitoring_router

# ----------------------------------------------------------------------
# 2. Definições Finais
# ----------------------------------------------------------------------

__version__ = "1.0.0"
__all__ = [
    # Router principal para inclusão no sistema FastAPI
    "monitoring_router",
    # Outros componentes (Modelos, Serviços, Schemas, etc.)
    "health_router",
    "metrics_router",
    "tracing_router",
    # Componentes de Business Logic
    "MonitoringService",  # Exemplo
    # ... adicione outros componentes importantes que devam ser exportados
]
