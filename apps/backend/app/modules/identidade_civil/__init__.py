"""
Módulo Identidade Civil (SILA)

Responsabilidades:
- Gerenciar requisições de documentos de identidade (BI, CEI, Atestados)
- Consultar dados biográficos soberanamente (via FUC)
- Processar eventos de ciclo de vida do documento

PRINCÍPIO DE SOBERANIA:
A Identidade Civil é consumidora de dados do FUC, nunca proprietária.
Qualquer alteração biográfica deve ocorrer exclusivamente no módulo FUC core.
"""

from fastapi import APIRouter

# Domain Entities
from .domain.models.citizen import Citizen
from .domain.models.bi import BI
from .domain.models.document import Document

# Infrastructure Models
from .infrastructure.models.citizen_model import CitizenModel

# Repositories
from .infrastructure.repositories.citizen_repository import CitizenRepository
from .infrastructure.repositories.document_repository import DocumentRepository

# Services
from .application.services.citizen_query_service import CitizenQueryService
from .application.services.alter_data_service import AlterDataService
from .application.services.bi_event_handler import handle_bi_event, event_handler

# Integrations
from .integrations.citizen_fuc_client import CitizenFUCClient

# API Routes
from .api.citizens.citizens_routes import router as citizens_router
from .api.documents.documents_routes import router as documents_router

# Utils
from app.core.utils.identity_safe import (
    safe_get,
    safe_getitem,
    safe_isoformat,
    safe_int,
    safe_float,
    safe_str,
    safe_bool,
)

# Exceptions
from .exceptions import (
    NotFoundException,
    BusinessRuleException,
    SovereigntyValidationException,
)

__all__ = [
    # Domain entities
    "Citizen",
    "BI",
    "Document",
    
    # Infrastructure models
    "CitizenModel",
    
    # Repositories
    "CitizenRepository",
    "DocumentRepository",
    
    # Services
    "CitizenQueryService",
    "AlterDataService",
    "handle_bi_event",
    "event_handler",
    
    # Integrations
    "CitizenFUCClient",
    
    # Utilities
    "safe_get",
    "safe_getitem",
    "safe_isoformat",
    "safe_int",
    "safe_float",
    "safe_str",
    "safe_bool",
    
    # Exceptions
    "NotFoundException",
    "BusinessRuleException",
    "SovereigntyValidationException",
]


def get_router() -> APIRouter:
    """
    Retorna o router com todas as rotas do módulo Identidade Civil.
    
    Returns:
        APIRouter configurado com rotas de cidadãos e documentos.
    """
    router = APIRouter(prefix="/identidade-civil", tags=["Identidade Civil"])
    router.include_router(citizens_router)
    router.include_router(documents_router)
    return router
