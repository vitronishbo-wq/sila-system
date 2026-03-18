from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.logistics.domain.enums import ModalTransporte, StatusLinha, StatusVeiculoOperacional, TipoVeiculo, TipoViagem

class LinhaCreate(BaseModel):
    nome: str
    modal: ModalTransporte
    tipo_viagem: TipoViagem
    origem: str
    destino: str
    itinerario: list[dict]
    extensao_km: Decimal
    tempo_estimado_minutos: int
    dias_operacao: list[str]
    horario_inicio: str
    horario_fim: str
    tarifa_base: Decimal
    operadora_id: UUID
    codigo: str | None = None
    frequencia_media_minutos: int | None = None
    codigo_corredor: str | None = None
    observacoes: str | None = None

class LinhaVincularVeiculoInput(BaseModel):
    placa: str

class LinhaTarifaInput(BaseModel):
    valor: Decimal

class LinhaIndicadoresInput(BaseModel):
    demanda_media_diaria: int | None = None
    ocupacao_media: Decimal | None = None
    regularidade: Decimal | None = None
    pontualidade: Decimal | None = None

class LinhaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo: str
    nome: str
    modal: ModalTransporte
    tipo_viagem: TipoViagem
    origem: str
    destino: str
    itinerario: list[dict] = Field(default_factory=list)
    extensao_km: Decimal
    tempo_estimado_minutos: int
    dias_operacao: list[str] = Field(default_factory=list)
    horario_inicio: str
    horario_fim: str
    tarifa_base: Decimal
    operadora_id: UUID
    status: StatusLinha
    data_cadastro: date
    data_atualizacao: date | None = None
    frota_operante: int | None = None
    demanda_media_diaria: int | None = None
    ocupacao_media: Decimal | None = None
    regularidade: Decimal | None = None
    pontualidade: Decimal | None = None
    observacoes: str | None = None
    veiculos_ativos: list[dict] = Field(default_factory=list)
    trilha_auditoria: list[dict] = Field(default_factory=list)

class VeiculoCreate(BaseModel):
    placa: str
    tipo: TipoVeiculo
    marca: str
    modelo: str
    ano_fabricacao: int
    ano_modelo: int
    proprietario_id: UUID
    proprietario_tipo: str
    data_aquisicao: date
    capacidade_passageiros: int | None = None
    operadora_id: UUID | None = None
    observacoes: str | None = None

class VeiculoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    placa: str
    tipo: TipoVeiculo
    marca: str
    modelo: str
    ano_fabricacao: int
    ano_modelo: int
    proprietario_id: UUID
    proprietario_tipo: str
    data_aquisicao: date
    status: StatusVeiculoOperacional
    capacidade_passageiros: int | None = None
    operadora_id: UUID | None = None
    quilometragem: int | None = None
    observacoes: str | None = None
    data_atualizacao: date | None = None