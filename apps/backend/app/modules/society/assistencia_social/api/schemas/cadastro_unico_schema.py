from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.society.assistencia_social.domain.enums import StatusCadastroUnico

class CadastroUnicoCreate(BaseModel):
    citizen_id_responsavel: UUID
    renda_per_capita: Decimal
    composicao_familiar: list[dict]
    condicoes_moradia: str
    acesso_agua: bool
    acesso_energia: bool
    observacoes: str | None = None

class CadastroUnicoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo: str
    citizen_id_responsavel: UUID
    renda_per_capita: Decimal
    composicao_familiar: list[dict]
    condicoes_moradia: str
    acesso_agua: bool
    acesso_energia: bool
    status: StatusCadastroUnico
    data_cadastro: date
    observacoes: str | None

class CadastroUnicoCreateResponse(BaseModel):
    cadastro: CadastroUnicoResponse
    programas_elegiveis: list[str]
    alertas: list[str]