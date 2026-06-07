from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID


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
    id: UUID
    codigo_med: str
    nome: str
    tipo: TipoEscola
    ciclos: list[CicloEnsino]
    provincia: str
    municipio: str
    comuna: str
    bairro: str
    endereco: str
    contacto: str | None = None
    email: str | None = None
    ativa: bool = True
