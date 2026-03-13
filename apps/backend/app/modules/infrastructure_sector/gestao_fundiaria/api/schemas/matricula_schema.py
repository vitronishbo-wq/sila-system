from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import StatusMatriculaImovel, TipoRegistro

class MatriculaCreate(BaseModel):
    imovel_inscricao: str
    tipo_registro: TipoRegistro
    cartorio_nome: str
    livro: str
    folha: str
    comarca: str
    provincia: str
    proprietario_documento: str | None = None
    numero_matricula: str | None = None

class MatriculaTransferenciaInput(BaseModel):
    novo_documento: str

class MatriculaMotivoInput(BaseModel):
    motivo: str

class MatriculaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_matricula: str
    imovel_inscricao: str
    tipo_registro: TipoRegistro
    cartorio_nome: str
    livro: str
    folha: str
    comarca: str
    provincia: str
    data_registro: date
    status: StatusMatriculaImovel
    ativo: bool
    proprietario_documento: str | None = None
    data_atualizacao: date | None = None
    observacoes: str | None = None