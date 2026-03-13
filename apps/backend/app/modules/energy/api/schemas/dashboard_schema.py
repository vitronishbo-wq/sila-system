from __future__ import annotations
from pydantic import BaseModel, Field
from app.modules.energy.api.schemas.central_geradora_schema import CentralGeradoraResponse
from app.modules.energy.api.schemas.linha_transmissao_schema import LinhaTransmissaoResponse
from app.modules.energy.api.schemas.subestacao_schema import SubestacaoResponse

class DashboardGeracaoResponse(BaseModel):
    centrais: list[CentralGeradoraResponse]
    subestacoes: list[SubestacaoResponse]
    linhas: list[LinhaTransmissaoResponse]
    errors: dict[str, str] = Field(default_factory=dict)
    degraded: bool = False
