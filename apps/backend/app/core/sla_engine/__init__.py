"""
SLA Engine Enterprise para SILA System
Gerencia SLAs hierárquicos, contextuais e adaptativos
"""

from .calculator import SLACalculator
from .models import (
    SLAContext,
    SLAResponse,
    SLAPriority,
    SLATier,
    CitizenType,
    Province,
    ChannelType,
    LoadLevel,
)
from .policies import SLAPolicyManager
from .governance import SLAGovernance
from .events import SLAEventEmitter
from .metrics import SLAMetrics

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
]
