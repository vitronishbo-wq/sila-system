"""
Módulo de Gestão Documental do SILA.

Este módulo fornece funcionalidades completas para:
- Gestão segura de documentos digitais
- Upload e armazenamento de arquivos
- Controle granular de acesso e permissões
- Organização hierárquica em pastas
- Busca avançada com filtros múltiplos
- Compartilhamento seguro com controle de uso
- Auditoria completa de todas as operações
- Versionamento e controle de alterações

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
    "DocumentService",
]

# Direct imports - apenas componentes essenciais
from . import models, schemas, services, endpoints

# Import service class - núcleo do negócio
try:
    from .services.document_service import DocumentService
except ImportError:
    # Para testes sem dependências completas
    DocumentService = None


def setup_documents_module(app) -> None:
    """
    Configura o módulo de documentos na aplicação FastAPI.

    Args:
        app: Instância da aplicação FastAPI
    """
    try:
        from fastapi import FastAPI

        # Import router here to avoid circular imports
        from .endpoints import router as documents_router

        # Include the router
        app.include_router(
            documents_router, prefix="/api/v1/documents", tags=["documents"]
        )

        # Log setup completion
        import logging

        logger = logging.getLogger(__name__)
        logger.info("Módulo de Gestão Documental configurado com sucesso")

    except ImportError as e:
        print(f"Aviso: FastAPI não disponível para configuração: {e}")
        print(
            "Módulo operacional para lógica de negócio, mas endpoints não configurados."
        )
