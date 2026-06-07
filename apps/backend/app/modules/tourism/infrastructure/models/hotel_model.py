from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from decimal import Decimal
from uuid import UUID

from apps.backend.app.modules.tourism.domain.enums import ClassificacaoHoteleira, TipoMeioHospedagem


@dataclass
class HotelModel:
    id: UUID
    cadastur: str
    nome: str
    tipo: TipoMeioHospedagem
    classificacao: ClassificacaoHoteleira
    cnpj: str
    endereco: str
    numero: str
    bairro: str
    municipio: str
    provincia: str
    cep: str
    telefone: str
    email: str
    quartos: int
    capacidade_maxima: int
    categoria_estrelas: int
    proprietario_id: UUID
    data_abertura: date
    inscricao_estadual: str | None = None
    inscricao_municipal: str | None = None
    complemento: str | None = None
    coordenadas_lat: Decimal | None = None
    coordenadas_long: Decimal | None = None
    site: str | None = None
    area_comum: list[str] | None = None
    servicos: list[str] | None = None
    acessibilidade: bool = False
    pet_friendly: bool = False
    wifi: bool = True
    estacionamento: bool = False
    piscina: bool = False
    academia: bool = False
    restaurante: bool = False
    bar: bool = False
    sala_reunioes: bool = False
    centro_convencoes: bool = False
    responsavel_id: UUID | None = None
    licenca_funcionamento: str | None = None
    data_renovacao: date | None = None
    observacoes: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
