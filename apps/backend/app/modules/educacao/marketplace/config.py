"""Marketplace module configuration"""
from enum import Enum
from typing import List


class MarketplaceLevel(str, Enum):
    """Níveis educacionais no marketplace"""
    BASICO = "basico"
    SECUNDARIO = "secundario"
    TECNICO = "tecnico"
    SUPERIOR = "superior"
    PROFISSIONAL = "profissional"


class MarketplaceModality(str, Enum):
    """Modalidades de programas"""
    PRESENCIAL = "presencial"
    REMOTO = "remoto"
    HIBRIDO = "hibrido"


class BookingStatus(str, Enum):
    """Estados de uma reserva"""
    RESERVED = "reserved"
    ENROLLED = "enrolled"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class AdmissionStatus(str, Enum):
    """Estados de uma admissão"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    PENDING_DOCUMENTS = "pending_documents"


class TransferStatus(str, Enum):
    """Estados de uma transferência"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


# Marketplace configuration
MARKETPLACE_CONFIG = {
    "subdomains": [
        "discovery",
        "ranking",
        "matching",
        "recommendation",
        "search",
        "booking",
        "transfers",
        "admissions",
    ],
    "booking_expiration_hours": 24,
    "matching_engine_version": "1.0",
    "recommendation_model_version": "1.0",
    "cache_ttl_seconds": 3600,
    "api_version": "v1",
}

# Validation rules
VALIDATION_RULES = {
    "opportunity": {
        "min_vacancies": 1,
        "max_vacancies": 10000,
        "required_fields": ["institution_id", "program_id", "level", "vacancies_total"],
    },
    "booking": {
        "max_per_citizen": 5,
        "expiration_hours": 24,
    },
    "transfer": {
        "min_credits_required": 30,
    },
}
