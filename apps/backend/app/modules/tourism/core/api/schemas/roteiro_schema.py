from __future__ import annotations
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class RoteiroCreate(BaseModel):
    titulo: str = Field(..., min_length=3)
    descricao: str = Field(..., min_length=5)
    municipio_origem: str
    provincia_origem: str
    duracao_horas: int = Field(..., gt=0)
    pontos_parada: list[str] | None = None
    acessivel: bool = True
    valor_estimado: Decimal | None = Field(default=None, ge=0)
    observacoes: str | None = None

class RoteiroUpdate(BaseModel):
    titulo: str | None = Field(default=None, min_length=3)
    descricao: str | None = Field(default=None, min_length=5)
    municipio_origem: str | None = None
    provincia_origem: str | None = None
    duracao_horas: int | None = Field(default=None, gt=0)
    pontos_parada: list[str] | None = None
    acessivel: bool | None = None
    valor_estimado: Decimal | None = Field(default=None, ge=0)
    observacoes: str | None = None
    ativo: bool | None = None
    refresh_integracoes: bool = True

class RoteiroResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo: str
    titulo: str
    descricao: str
    municipio_origem: str
    provincia_origem: str
    duracao_horas: int
    pontos_parada: list[str]
    acessivel: bool
    ativo: bool
    valor_estimado: Decimal | None = None
    meios_transporte_sugeridos: list[str] | None = None
    parceiros_comerciais: list[str] | None = None
    observacoes: str | None = None