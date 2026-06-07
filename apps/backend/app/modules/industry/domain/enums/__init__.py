"""Domain enumerations module"""

from enum import Enum

from .status_enum import AuditStatus, EntityStatus, LifecycleStatus, ProcessStatus
from .type_enum import (
    DocumentType,
    EntityType,
    NotificationPriority,
    OperationType,
    SortOrder,
    ValidationLevel,
)

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
    "RamoIndustrial",
    "PorteIndustrial",
    "TipoEstabelecimento",
    "StatusEstabelecimento",
]


class RamoIndustrial(Enum):
    EXTRATIVA = "extrativa"
    TRANSFORMACAO = "transformacao"
    ALIMENTAR = "alimentar"
    BEBIDAS = "bebidas"
    TEXTIL = "textil"
    QUIMICA = "quimica"
    METALURGICA = "metalurgica"
    ELETRONICA = "eletronica"
    VEICULOS = "veiculos"


class PorteIndustrial(Enum):
    MICRO = "micro"
    PEQUENA = "pequena"
    MEDIA = "media"
    GRANDE = "grande"


class TipoEstabelecimento(Enum):
    MATRIZ = "matriz"
    FILIAL = "filial"
    UNIDADE = "unidade"


class StatusEstabelecimento(Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    SUSPENSO = "suspenso"
    LICENCIAMENTO = "licenciamento"
    CONSTRUCAO = "construcao"
    PARALISADO = "paralisado"
