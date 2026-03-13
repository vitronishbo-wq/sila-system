from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID

@dataclass
class AgenciaViagensModel:
    id: UUID
    registro: str
    nome_fantasia: str
    razao_social: str
    cnpj: str
    email: str
    telefone: str
    endereco: str
    numero: str
    bairro: str
    municipio: str
    provincia: str
    cep: str
    proprietario_id: UUID
    data_registro: date
    ativa: bool = True
    especialidades: list[str] | None = None
    site: str | None = None
    observacoes: str | None = None