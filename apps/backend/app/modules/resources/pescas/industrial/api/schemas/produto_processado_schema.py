from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.modules.resources.pescas.industrial.domain.enums import MercadoDestino, TipoProcessamento, TipoProdutoProcessado

class ProdutoProcessadoCreate(BaseModel):
    unidade_processamento_id: UUID
    nome_comercial: str = Field(..., min_length=2)
    tipo_produto: TipoProdutoProcessado
    tipo_processamento: TipoProcessamento
    peso_liquido_kg: Decimal = Field(..., gt=0)
    rendimento_percentual: Decimal = Field(..., gt=0, le=100)
    mercado_destino: MercadoDestino
    observacoes: str | None = None

class ProdutoProcessadoUpdate(BaseModel):
    nome_comercial: str | None = Field(default=None, min_length=2)
    tipo_produto: TipoProdutoProcessado | None = None
    tipo_processamento: TipoProcessamento | None = None
    peso_liquido_kg: Decimal | None = Field(default=None, gt=0)
    rendimento_percentual: Decimal | None = Field(default=None, gt=0, le=100)
    mercado_destino: MercadoDestino | None = None
    ativo: bool | None = None
    observacoes: str | None = None

class ProdutoProcessadoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_produto: str
    unidade_processamento_id: UUID
    nome_comercial: str
    tipo_produto: TipoProdutoProcessado
    tipo_processamento: TipoProcessamento
    peso_liquido_kg: Decimal
    rendimento_percentual: Decimal
    mercado_destino: MercadoDestino
    data_registro: date
    ativo: bool
    observacoes: str | None = None