
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID, uuid4


class TipoEscola(StrEnum):
    PUBLICA = "publica"
    PRIVADA = "privada"
    PUBLICO_PRIVADA = "publico_privada"
    COMUNITARIA = "comunitaria"


class CicloEnsino(StrEnum):
    PRE_ESCOLAR = "pre_escolar"
    PRIMARIO = "primario"
    SECUNDARIO_1 = "secundario_1"
    SECUNDARIO_2 = "secundario_2"
    TECNICO = "tecnico"
    FORMACAO = "formacao"


@dataclass
class Escola:
    id: UUID = field(default_factory=uuid4)
    codigo_med: str
    nome: str
    tipo: TipoEscola
    ciclos: list[CicloEnsino]
    territory_id: UUID  # Princípio 8 e 9: Apenas a referência direta
    endereco: str
    created_by: UUID  # Princípio 8
    managed_by: UUID  # Princípio 8
    contacto: str | None = None
    email: str | None = None
    ativa: bool = True
