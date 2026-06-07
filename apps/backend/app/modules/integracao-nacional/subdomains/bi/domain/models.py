from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class BiStatus(str, Enum):
    VALIDO = "valido"
    EXPIRADO = "expirado"
    CANCELADO = "cancelado"
    SUSPENSO = "suspenso"
    NAO_ENCONTRADO = "nao_encontrado"
    PENDENTE = "pendente"


class BiTipo(str, Enum):
    NORMAL = "normal"
    ESTRANGEIRO = "estrangeiro"
    DIPLOMATICO = "diplomatico"
    PROVISORIO = "provisorio"


@dataclass
class BilheteIdentidade:
    numero: str
    full_name: str
    birth_date: str
    gender: str
    filiation_pai: Optional[str] = None
    filiation_mae: Optional[str] = None
    nationality: str = "ANGOLANA"
    tipo: BiTipo = BiTipo.NORMAL
    status: BiStatus = BiStatus.VALIDO
    emission_date: Optional[str] = None
    expiration_date: Optional[str] = None
    emission_place: Optional[str] = None
    nif: Optional[str] = None
    photo_hash: Optional[str] = None
    fingerprint_hash: Optional[str] = None


@dataclass
class BiVerificationResult:
    bi_numero: str
    valido: bool
    status: BiStatus
    cidadao_encontrado: bool
    dados: Optional[BilheteIdentidade] = None
    id: UUID = field(default_factory=uuid4)
    verificacao_timestamp: datetime = field(default_factory=datetime.utcnow)
    fonte: str = "direta"
    confidence: float = 1.0


@dataclass
class BiConsultaResult:
    bi_numero: str
    encontrado: bool
    dados: Optional[BilheteIdentidade] = None
    id: UUID = field(default_factory=uuid4)
    consulta_timestamp: datetime = field(default_factory=datetime.utcnow)
