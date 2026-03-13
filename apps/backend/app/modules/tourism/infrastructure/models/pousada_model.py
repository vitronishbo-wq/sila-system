from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID
from app.modules.tourism.domain.enums import ClassificacaoHoteleira, TipoMeioHospedagem

@dataclass
class PousadaModel:
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
    proprietario_id: UUID
    data_abertura: date
    ativa: bool = True
    site: str | None = None
    observacoes: str | None = None
