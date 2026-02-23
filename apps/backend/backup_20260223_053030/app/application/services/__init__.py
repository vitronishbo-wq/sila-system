"""Services do módulo de registo civil"""

from .base_service import BaseService
from .birth_service import BirthService
from .death_service import DeathService
from .marriage_service import MarriageService
from .certificate_service import CertificateService
from .civil_query_service import CivilQueryService

__all__ = [
    "BaseService",
    "BirthService",
    "DeathService",
    "MarriageService",
    "CertificateService",
    "CivilQueryService"
]
