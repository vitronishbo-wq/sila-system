"""
Módulo de Cidadania do SILA.
Focado na exportação limpa de componentes e exceções.
"""

from . import crud, models, schemas, services, endpoints
from .exceptions import (
    AddressValidationError,
    CitizenNotFoundError,
    CitizenshipError,
    DocumentNotFoundError,
    DocumentVerificationError,
    DuplicateCitizenError,
    InvalidDocumentError,
)
from .handlers import (
    ERROR_RESPONSES,
    citizenship_exception_handler,
    register_exception_handlers,
    setup_error_handling,
)
from .services.citizenship_service import CitizenshipService

__all__ = [
    "CitizenshipError",
    "CitizenNotFoundError",
    "DocumentNotFoundError",
    "DuplicateCitizenError",
    "InvalidDocumentError",
    "DocumentVerificationError",
    "AddressValidationError",
    "citizenship_exception_handler",
    "register_exception_handlers",
    "setup_error_handling",
    "ERROR_RESPONSES",
    "crud",
    "schemas",
    "models",
    "services",
    "endpoints",
    "CitizenshipService",
]
