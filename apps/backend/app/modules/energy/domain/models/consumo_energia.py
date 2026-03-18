from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.energy.domain.enums import TipoLeituraEnergia

@dataclass
class ConsumoEnergia:
    id: UUID
    unidade_consumidora_id: UUID
    medidor_id: UUID | None
    data_leitura: datetime
    leitura_kwh: Decimal
    leitura_anterior_kwh: Decimal | None
    consumo_periodo_kwh: Decimal
    tipo_leitura: TipoLeituraEnergia
    classe_tarifaria: str
    cpf_titular: str

    @classmethod
    def registrar(cls, *, unidade_consumidora_id: UUID, data_leitura: datetime, leitura_kwh: Decimal, tipo_leitura: TipoLeituraEnergia, classe_tarifaria: str, cpf_titular: str, medidor_id: UUID | None=None, leitura_anterior_kwh: Decimal | None=None) -> 'ConsumoEnergia':
        if leitura_kwh < Decimal('0'):
            raise ValueError('Leitura kWh nao pode ser negativa')
        if not classe_tarifaria.strip():
            raise ValueError('Classe tarifaria e obrigatoria')
        if not cpf_titular.strip():
            raise ValueError('CPF do titular e obrigatorio')
        if leitura_anterior_kwh is None:
            consumo = Decimal('0')
        else:
            consumo = leitura_kwh - leitura_anterior_kwh
            if consumo < Decimal('0'):
                raise ValueError('Leitura atual nao pode ser menor que leitura anterior')
        return cls(id=uuid4(), unidade_consumidora_id=unidade_consumidora_id, medidor_id=medidor_id, data_leitura=data_leitura, leitura_kwh=leitura_kwh.quantize(Decimal('0.01')), leitura_anterior_kwh=leitura_anterior_kwh.quantize(Decimal('0.01')) if leitura_anterior_kwh is not None else None, consumo_periodo_kwh=consumo.quantize(Decimal('0.01')), tipo_leitura=tipo_leitura, classe_tarifaria=classe_tarifaria.strip().lower(), cpf_titular=cpf_titular.strip())