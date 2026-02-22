"""Health Module

This module provides health-related functionality including:
- Health record management
- Medical appointment scheduling
- Health data tracking and reporting
"""

"""Module initialization with path configuration."""

import sys
from pathlib import Path

# Ensure backend is in path for imports
_backend_path = Path(__file__).parent.parent.parent
if str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

from .schemas import HealthBase, HealthCreate, HealthInDB, HealthUpdate

# Import HealthService directly from the services.py file to avoid confusion with the services directory
from .services import HealthService

__all__ = [
    # Schemas
    "HealthBase",
    "HealthCreate",
    "HealthUpdate",
    "HealthInDB",
    # Services
    "HealthService",
    # Modules
    "models",
    "schemas",
    "routes",
    "tests",
    "handlers",
    "exceptions",
]
# Serviço: Agendamento de Consulta Médica / Medical Appointment Booking

# Serviço: Solicitação de Exame Laboratorial / Laboratory Test Request

# Serviço: Agendamento de Vacinação / Vaccination Scheduling

# Serviço: Cartão de Vacinação Digital / Digital Vaccination Card

# Serviço: Teleconsulta Médica / Telemedicine Consultation

# Serviço: Solicitação de Medicamento / Medication Request

# Serviço: Histórico Médico Digital / Digital Medical History

# Serviço: Seguro de Saúde Municipal / Municipal Health Insurance

# Serviço: Serviço de Emergência Médica / Medical Emergency Service

# Serviço: Avaliação Nutricional / Nutritional Assessment
