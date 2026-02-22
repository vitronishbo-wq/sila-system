"""
Módulo de Analytics do SILA.

Este módulo fornece funcionalidades completas para:
- Dashboards executivos com KPIs estratégicos
- Relatórios personalizáveis e análises de dados
- Métricas em tempo real e indicadores de performance
- Sistema de alertas inteligentes baseados em thresholds
- Cache inteligente para performance otimizada
- Análise de tendências e forecasting básico
- Exportação de dados em múltiplos formatos
- Auditoria completa de consultas e uso de dados

NOTA: Para evitar problemas de dependências durante testes,
as importações de FastAPI são feitas apenas quando necessário.
"""

"""Module initialization with path configuration."""

import sys
from pathlib import Path

# Ensure backend is in path for imports
_backend_path = Path(__file__).parent.parent.parent
if str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

# Core exports - apenas modelos e lógica de negócio
__all__ = [
    # Modules
    "models",
    "schemas",
    "services",
    "endpoints",
    # Service classes
    "AnalyticsService",
]

# Direct imports - apenas componentes essenciais
from . import models, schemas, services, endpoints

# Import service class - núcleo do negócio
try:
    from .services.analytics_service import AnalyticsService
except ImportError:
    # Para testes sem dependências completas
    AnalyticsService = None


def setup_analytics_module(app) -> None:
    """
    Configura o módulo de analytics na aplicação FastAPI.

    Args:
        app: Instância da aplicação FastAPI
    """
    try:
        from fastapi import FastAPI

        # Import router here to avoid circular imports
        from .endpoints import router as analytics_router

        # Include the router
        app.include_router(
            analytics_router, prefix="/api/v1/analytics", tags=["analytics"]
        )

        # Log setup completion
        import logging

        logger = logging.getLogger(__name__)
        logger.info("Módulo de Analytics configurado com sucesso")

    except ImportError as e:
        print(f"Aviso: FastAPI não disponível para configuração: {e}")
        print(
            "Módulo operacional para lógica de negócio, mas endpoints não configurados."
        )
