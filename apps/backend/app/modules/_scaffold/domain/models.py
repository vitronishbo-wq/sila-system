from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class RegistoStatus(str, Enum):
    PENDENTE = "pendente"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"
    RETIFICADO = "retificado"


class TipoRegisto(str, Enum):
    NASCIMENTO = "nascimento"
    OBITO = "obito"
    CASAMENTO = "casamento"


@dataclass
class RegistoNascimento:
    id: UUID = field(default_factory=uuid4)
    nome_completo: str = ""
    data_nascimento: str = ""
    genero: str = ""
    naturalidade: str = ""
    nome_pai: Optional[str] = None
    nome_mae: Optional[str] = None
    bi_pai: Optional[str] = None
    bi_mae: Optional[str] = None
    local_nascimento: Optional[str] = None
    provincia: str = ""
    municipio: str = ""
    status: RegistoStatus = RegistoStatus.PENDENTE
    registado_por: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class RegistoObito:
    id: UUID = field(default_factory=uuid4)
    falecido_nome: str = ""
    falecido_bi: str = ""
    data_obito: str = ""
    causa: Optional[str] = None
    local_obito: Optional[str] = None
    provincia: str = ""
    municipio: str = ""
    certidao_medica: Optional[str] = None
    status: RegistoStatus = RegistoStatus.PENDENTE
    registado_por: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class RegistoCasamento:
    id: UUID = field(default_factory=uuid4)
    conjuge1_nome: str = ""
    conjuge1_bi: str = ""
    conjuge2_nome: str = ""
    conjuge2_bi: str = ""
    data_casamento: str = ""
    regime_bens: str = "comunhao_geral"
    local_casamento: Optional[str] = None
    provincia: str = ""
    municipio: str = ""
    status: RegistoStatus = RegistoStatus.PENDENTE
    registado_por: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
