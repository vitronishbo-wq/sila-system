from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class MoradaTipo(str, Enum):
    RESIDENCIAL = "residencial"
    COMERCIAL = "comercial"
    FISCAL = "fiscal"
    CORRESPONDENCIA = "correspondencia"
    OUTRO = "outro"


@dataclass
class Morada:
    linha1: str
    bairro: Optional[str] = None
    comuna: Optional[str] = None
    municipio: str = ""
    provincia: str = ""
    codigo_postal: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    tipo: MoradaTipo = MoradaTipo.RESIDENCIAL


@dataclass
class MoradaNormalizada:
    original: str
    linha1: str
    id: UUID = field(default_factory=uuid4)
    bairro: Optional[str] = None
    comuna: Optional[str] = None
    municipio: Optional[str] = None
    provincia: Optional[str] = None
    codigo_postal: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    confidence: float = 0.0
    normalizada_em: datetime = field(default_factory=datetime.utcnow)


@dataclass
class MoradaValidationResult:
    valida: bool
    confianca: float
    problemas: list[str] = field(default_factory=list)
    sugestoes: list[str] = field(default_factory=list)
