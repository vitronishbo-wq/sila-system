from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from uuid import UUID

class TipoEscola(str, Enum):
    PUBLICA = 'publica'
    PRIVADA = 'privada'
    PUBLICO_PRIVADA = 'publico_privada'
    COMUNITARIA = 'comunitaria'

class CicloEnsino(str, Enum):
    PRE_ESCOLAR = 'pre_escolar'
    PRIMARIO = 'primario'
    SECUNDARIO_1 = 'secundario_1'
    SECUNDARIO_2 = 'secundario_2'
    TECNICO = 'tecnico'
    FORMACAO = 'formacao'

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
    contacto: Optional[str] = None
    email: Optional[str] = None
    ativa: bool = True