from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.logistics.domain.enums import StatusFrota, TipoTarifa

class FrotaCreate(BaseModel):
    nome: str
    operadora_id: UUID
    municipio: str
    provincia: str
    codigo_frota: str | None = None
    observacoes: str | None = None

class FrotaAdicionarVeiculoInput(BaseModel):
    veiculo_id: UUID
    placa: str
    tipo: str
    capacidade: int | None = None

class FrotaManutencaoInput(BaseModel):
    veiculo_id: UUID
    tipo: str
    oficina: str
    custo: Decimal
    data_manutencao: date | None = None
    observacoes: str | None = None

class FrotaTarifaInput(BaseModel):
    tipo_tarifa: TipoTarifa
    valor: Decimal
    motivo: str
    data_inicio_vigencia: date | None = None
    data_fim_vigencia: date | None = None

class FrotaFiscalizacaoInput(BaseModel):
    fiscal_id: UUID
    conformidade: bool
    apontamentos: str
    data_fiscalizacao: date | None = None
    auto_infracao: str | None = None
    observacoes: str | None = None

class FrotaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_frota: str
    nome: str
    operadora_id: UUID
    municipio: str
    provincia: str
    status: StatusFrota
    data_cadastro: date
    data_atualizacao: date | None = None
    observacoes: str | None = None
    veiculos: list[dict] = Field(default_factory=list)
    manutencoes: list[dict] = Field(default_factory=list)
    fiscalizacoes: list[dict] = Field(default_factory=list)
    tarifas: list[dict] = Field(default_factory=list)
    trilha_auditoria: list[dict] = Field(default_factory=list)
