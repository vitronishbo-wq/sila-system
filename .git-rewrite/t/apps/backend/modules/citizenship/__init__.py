"""
Módulo de Cidadania do SILA.

Este módulo fornece funcionalidades para gerenciar cidadãos, documentos e feedbacks,
além de validações e regras de negócio relacionadas à cidadania.
"""

"""Module initialization with path configuration."""

import sys
from pathlib import Path

# Ensure backend is in path for imports
_backend_path = Path(__file__).parent.parent.parent
if str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

from typing import Any, Dict, List, Optional, Type, Union

from fastapi import FastAPI, HTTPException, Request, status

# Core exports
__all__ = [
    # Exception classes
    "CitizenshipError",
    "CitizenNotFoundError",
    "DocumentNotFoundError",
    "DuplicateCitizenError",
    "InvalidDocumentError",
    "DocumentVerificationError",
    "AddressValidationError",
    # Handler functions
    "citizenship_exception_handler",
    "register_exception_handlers",
    "setup_error_handling",
    "setup_citizenship_module",
    "ERROR_RESPONSES",
    # Modules
    "crud",
    "schemas",
    "models",
    "services",
    "endpoints",
    # Service classes
    "CitizenshipService",
]

# Direct imports
from . import crud, models, schemas, services, endpoints

# Import exceptions
from .exceptions import (
    AddressValidationError,
    CitizenNotFoundError,
    CitizenshipError,
    DocumentNotFoundError,
    DocumentVerificationError,
    DuplicateCitizenError,
    InvalidDocumentError,
)

# Import handlers
from .handlers import (
    ERROR_RESPONSES,
    citizenship_exception_handler,
    register_exception_handlers,
    setup_error_handling,
)

# Import service class
from .services.citizenship_service import CitizenshipService


def setup_citizenship_module(app: FastAPI) -> None:
    """
    Configura o módulo de cidadania na aplicação FastAPI.

    Args:
        app: Instância da aplicação FastAPI
    """
    # Configure error handling
    setup_error_handling(app)

    # Import router here to avoid circular imports
    from .endpoints import router as citizenship_router

    # Include the router
    app.include_router(citizenship_router, prefix="/api/v1", tags=["citizenship"])

    # Log setup completion
    import logging

    logger = logging.getLogger(__name__)
    logger.info("Módulo de Cidadania configurado com sucesso")
