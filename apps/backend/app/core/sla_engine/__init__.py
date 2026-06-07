"""
SLA Engine Enterprise para SILA System
Gerencia SLAs hierárquicos, contextuais e adaptativos
"""

from .admin import router as sla_admin_router
from .api import router as sla_router
from .calculator import SLACalculator
from .events import SLAEventEmitter
from .governance import SLAGovernance
from .metrics import SLAMetrics
from .models import (
    ChannelType,
    CitizenType,
    LoadLevel,
    Province,
    SLAContext,
    SLAPriority,
    SLAResponse,
    SLATier,
)
from .policies import SLAPolicyManager

__version__ = "2.0.0"

__all__ = [
    "SLACalculator",
    "SLAContext",
    "SLAResponse",
    "SLAPriority",
    "SLATier",
    "CitizenType",
    "Province",
    "ChannelType",
    "LoadLevel",
    "SLAPolicyManager",
    "SLAGovernance",
    "SLAEventEmitter",
    "SLAMetrics",
    "sla_router",
    "sla_admin_router",
]
