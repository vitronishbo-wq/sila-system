from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.energy.domain.enums import FonteEnergia, StatusUsina, TipoUsina

@dataclass
class UsinaModel:
    id: UUID
    codigo_aneel: str
    nome: str
    fonte: FonteEnergia
    tipo: TipoUsina
    status: StatusUsina
    potencia_instalada_mw: Decimal
    proprietario_id: UUID
    proprietario_tipo: str
    municipio: str
    provincia: str
    potencia_fiscalizada_mw: Decimal | None = None
    garantia_fisica_mw: Decimal | None = None
    energia_assegurada_mwm: Decimal | None = None
    operador_id: UUID | None = None
    concessionaria_id: UUID | None = None
    outorga_id: UUID | None = None
    licenca_operacao_id: UUID | None = None
    data_autorizacao: date | None = None
    data_inicio_construcao: date | None = None
    data_entrada_operacao: date | None = None
    data_validade_outorga: date | None = None
    observacoes: str | None = None