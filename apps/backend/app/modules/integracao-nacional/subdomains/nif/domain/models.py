from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class NifStatus(str, Enum):
    ATIVO = "ativo"
    SUSPENSO = "suspenso"
    CANCELADO = "cancelado"
    NAO_ENCONTRADO = "nao_encontrado"


class NifTipoContribuinte(str, Enum):
    SINGULAR = "singular"
    COLETIVA = "coletiva"
    PUBLICO = "publico"
    ESTRANGEIRO = "estrangeiro"


@dataclass
class NifData:
    nif: str
    full_name: str
    tipo: NifTipoContribuinte
    status: NifStatus
    bi_numero: Optional[str] = None
    email: Optional[str] = None
    morada: Optional[str] = None
    telefone: Optional[str] = None
    atividade_economica: Optional[str] = None
    regime_iva: Optional[str] = None


@dataclass
class NifVerificationResult:
    nif: str
    valido: bool
    status: NifStatus
    contribuinte_encontrado: bool
    dados: Optional[NifData] = None
    id: UUID = field(default_factory=uuid4)
    verificacao_timestamp: datetime = field(default_factory=datetime.utcnow)
