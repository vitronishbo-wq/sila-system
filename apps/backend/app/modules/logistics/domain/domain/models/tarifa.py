from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.logistics.domain.enums import TipoTarifa

@dataclass
class Tarifa:
    id: UUID
    tipo: TipoTarifa
    valor: Decimal
    data_inicio_vigencia: date
    motivo: str
    data_fim_vigencia: date | None = None

    @classmethod
    def definir(cls, *, tipo: TipoTarifa, valor: Decimal, data_inicio_vigencia: date | None=None, data_fim_vigencia: date | None=None, motivo: str) -> 'Tarifa':
        if valor <= Decimal('0'):
            raise ValueError('Valor de tarifa deve ser maior que zero')
        if not motivo.strip():
            raise ValueError('Motivo da definicao de tarifa e obrigatorio')
        if data_fim_vigencia and data_inicio_vigencia and (data_fim_vigencia <= data_inicio_vigencia):
            raise ValueError('Data fim da vigencia deve ser maior que data inicio')
        inicio = data_inicio_vigencia or date.today()
        return cls(id=uuid4(), tipo=tipo, valor=valor.quantize(Decimal('0.01')), data_inicio_vigencia=inicio, data_fim_vigencia=data_fim_vigencia, motivo=motivo.strip())

    def to_dict(self) -> dict:
        return {'id': str(self.id), 'tipo': self.tipo.value, 'valor': str(self.valor), 'data_inicio_vigencia': self.data_inicio_vigencia.isoformat(), 'data_fim_vigencia': self.data_fim_vigencia.isoformat() if self.data_fim_vigencia else None, 'motivo': self.motivo}
