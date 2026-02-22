"""Module initialization with path configuration."""

import sys
from pathlib import Path

# Ensure backend is in path for imports
_backend_path = Path(__file__).parent.parent.parent
if str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

from .routes import router

__all__ = ["router", "models", "schemas", "services"]


# Serviço: Relatório de KPI / KPI Report

# Serviço: Análise de Dados / Data Analysis

# Serviço: Dashboard Executivo / Executive Dashboard

# Serviço: Métricas de Uso / Usage Metrics

# Serviço: Estatísticas SILA Dashboard / SILA Dashboard Statistics
