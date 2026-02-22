"""Módulo de Reclamações (Complaints)

Este módulo fornece funcionalidades para gerenciar reclamações, incluindo:
- Criação e gerenciamento de reclamações
- Categorização de reclamações
- Comentários em reclamações
- Estatísticas e relatórios
"""

"""Module initialization with path configuration."""

import sys
from pathlib import Path

# Ensure backend is in path for imports
_backend_path = Path(__file__).parent.parent.parent
if str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

from .crud import ComplaintCRUD
from .models import (
    ComplaintCategoryCreate,
    ComplaintCategoryResponse,
    ComplaintCategoryUpdate,
    ComplaintCommentCreate,
    ComplaintCommentResponse,
    ComplaintCreate,
    ComplaintFilter,
    ComplaintResponse,
    ComplaintStats,
    ComplaintUpdate,
)
from .services import ComplaintService

__all__ = [
    "ComplaintService",
    "ComplaintCRUD",
    "models",
    "schemas",
    "crud",
    "services",
    "endpoints",
    "ComplaintCreate",
    "ComplaintUpdate",
    "ComplaintResponse",
    "ComplaintCommentCreate",
    "ComplaintCommentResponse",
    "ComplaintCategoryCreate",
    "ComplaintCategoryUpdate",
    "ComplaintCategoryResponse",
    "ComplaintFilter",
    "ComplaintStats",
]


# Serviço: Denúncia Cidadã / Citizen Report

# Serviço: Ouvidoria Municipal / Municipal Ombudsman

# Serviço: Reclamação de Serviço / Service Complaint

# Serviço: Sugestão de Melhoria / Improvement Suggestion

# Serviço: Fiscalização de Obra / Construction Oversight

# Serviço: Denúncia Ambiental / Environmental Report

# Serviço: Violação de Direitos / Rights Violation

# Serviço: Corrupção Administrativa / Administrative Corruption

# Serviço: Mau Atendimento / Poor Service

# Serviço: Irregularidade Fiscal / Tax Irregularity
