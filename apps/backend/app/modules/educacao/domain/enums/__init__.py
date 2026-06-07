"""Domain enumerations module"""

from enum import StrEnum

from .status_enum import AuditStatus, EntityStatus, LifecycleStatus, ProcessStatus
from .type_enum import (
    DocumentType,
    EntityType,
    NotificationPriority,
    OperationType,
    SortOrder,
    ValidationLevel,
)


class StatusFluxo(StrEnum):
    """Status values for workflow/transfer"""
    PENDENTE = "pendente"
    CONFIRMADA = "confirmada"
    EM_ANALISE = "em_analise"
    APROVADA = "aprovada"
    REJEITADA = "rejeitada"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"


class TipoInscricao(StrEnum):
    """Types of inscription/enrollment"""
    BASICA = "basica"
    SECUNDARIA = "secundaria"
    SUPERIOR = "superior"
    TECNICO = "tecnico"


__all__ = [
    "EntityStatus",
    "ProcessStatus",
    "LifecycleStatus",
    "AuditStatus",
    "EntityType",
    "DocumentType",
    "OperationType",
    "SortOrder",
    "NotificationPriority",
    "ValidationLevel",
    "StatusFluxo",
    "TipoInscricao",
]
