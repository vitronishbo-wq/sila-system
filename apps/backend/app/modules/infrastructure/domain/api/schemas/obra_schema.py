from __future__ import annotations
from datetime import date
from decimal import Decimal
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.modules.infrastructure.domain.enums import NaturezaObra, StatusObra, TipoObra

class ObraCreate(BaseModel):
    nome: str
    tipo: TipoObra
    natureza: NaturezaObra
    orgao_responsavel_id: UUID
    orgao_responsavel_tipo: str
    valor_orcado: Decimal
    data_inicio_prevista: date
    data_fim_prevista: date
    endereco: str
    bairro: str
    municipio: str
    provincia: str
    codigo_obra: str | None = None
    descricao: str | None = None

class ObraContratacaoInput(BaseModel):
    contrato_id: UUID
    empreiteira_id: UUID
    valor_contratado: Decimal

class ObraInicioExecucaoInput(BaseModel):
    data_inicio: date

class ObraProgressoInput(BaseModel):
    percentual: Decimal

class ObraValorInput(BaseModel):
    valor: Decimal

class ObraSuspensaoInput(BaseModel):
    motivo: str

class ObraConclusaoInput(BaseModel):
    data_conclusao: date

class ObraEntregaInput(BaseModel):
    data_entrega: date

class ObraMedicaoDetalhadaInput(BaseModel):
    periodo_referencia: str
    valor_medido: Decimal
    percentual_executado: Decimal
    fiscal_id: UUID
    documentos: list[str] = Field(default_factory=list)
    observacoes: str | None = None
    data_medicao: date | None = None

class ObraAditivoInput(BaseModel):
    tipo: Literal['prazo', 'valor', 'objeto', 'ambos']
    justificativa: str
    valor_aditivo: Decimal = Decimal('0')
    prazo_adicional_dias: int = 0
    data_assinatura: date | None = None

class ObraFiscalizacaoInput(BaseModel):
    fiscal_id: UUID
    conformidade: bool
    apontamentos: str
    recomendacoes: str | None = None
    data_fiscalizacao: date | None = None

class ObraTermoRecebimentoInput(BaseModel):
    tipo: Literal['provisorio', 'definitivo']
    responsavel_id: UUID
    data_termo: date | None = None
    observacoes: str | None = None

class ObraResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_obra: str
    nome: str
    tipo: TipoObra
    natureza: NaturezaObra
    status: StatusObra
    orgao_responsavel_id: UUID
    orgao_responsavel_tipo: str
    valor_orcado: Decimal
    data_inicio_prevista: date
    data_fim_prevista: date
    endereco: str
    bairro: str
    municipio: str
    provincia: str
    prazo_original_dias: int
    data_cadastro: date
    descricao: str | None = None
    gestor_responsavel_id: UUID | None = None
    fiscal_responsavel_id: UUID | None = None
    empreiteira_id: UUID | None = None
    contrato_id: UUID | None = None
    projeto_id: UUID | None = None
    valor_contratado: Decimal | None = None
    valor_executado: Decimal | None = None
    valor_pago: Decimal | None = None
    data_inicio_real: date | None = None
    data_fim_real: date | None = None
    data_entrega: date | None = None
    coordenadas_lat: Decimal | None = None
    coordenadas_long: Decimal | None = None
    imovel_id: UUID | None = None
    percentual_executado: Decimal
    prazo_adicionado_dias: int
    dias_corridos: int
    dias_atraso: int
    data_atualizacao: date | None = None
    observacoes: str | None = None
    medicoes: list[dict] = Field(default_factory=list)
    aditivos: list[dict] = Field(default_factory=list)
    fiscalizacoes: list[dict] = Field(default_factory=list)
    termos_recebimento: list[dict] = Field(default_factory=list)
    trilha_auditoria: list[dict] = Field(default_factory=list)

class ObraDashboardReadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    obra_id: str
    tenant_id: str
    codigo: str
    status: str
    valor_total: Decimal
    valor_executado: Decimal
    percentual_execucao: Decimal

class EventStoreEntryResponse(BaseModel):
    id: str
    aggregate_id: str
    aggregate_type: str
    event_type: str
    event_data: dict
    version: int
    tenant_id: str
    region_code: str
    correlation_id: str
    created_at: str | None = None

class ObraRehydratedStateResponse(BaseModel):
    obra_id: str
    codigo_obra: str
    status: str
    valor_total: str
    valor_executado: str
    event_count: int
