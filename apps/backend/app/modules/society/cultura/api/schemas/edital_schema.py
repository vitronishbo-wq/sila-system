from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.modules.society.cultura.domain.enums import FaseEditalCultural, TipoEditalCultural

class EditalCreate(BaseModel):
    numero: str = Field(..., min_length=3)
    titulo: str = Field(..., min_length=5)
    tipo: TipoEditalCultural
    orgao_responsavel_id: UUID
    valor_total: Decimal = Field(..., gt=0)
    data_publicacao: datetime
    data_inicio_inscricoes: datetime
    data_fim_inscricoes: datetime
    vagas: int = Field(..., gt=0)
    descricao: str = Field(..., min_length=10)
    criterios: list[str] = Field(default_factory=list)
    documentos_necessarios: list[str] = Field(default_factory=list)

class EditalSelecaoRequest(BaseModel):
    projetos_ids: list[UUID]

class EditalInscricaoRequest(BaseModel):
    projeto_id: UUID

class EditalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero: str
    titulo: str
    tipo: TipoEditalCultural
    orgao_responsavel_id: UUID
    valor_total: Decimal
    valor_disponivel: Decimal
    data_publicacao: datetime
    data_inicio_inscricoes: datetime
    data_fim_inscricoes: datetime
    vagas: int
    descricao: str
    fase: FaseEditalCultural
    criterios: list[str]
    documentos_necessarios: list[str]
    inscricoes: list[UUID]
    projetos_selecionados: list[UUID]
    ativo: bool