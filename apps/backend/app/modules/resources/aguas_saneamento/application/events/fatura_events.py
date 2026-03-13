from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.resources.aguas_saneamento.domain.models.fatura_agua import FaturaAgua

def _to_iso_date(value: date) -> str:
    return value.isoformat()

def _from_iso_date(value: str) -> date:
    return date.fromisoformat(value)

@dataclass(frozen=True)
class FaturaEmitidaEvent:
    event_id: UUID
    occurred_at: datetime
    fatura_id: UUID
    numero_fatura: str
    consumo_id: UUID
    titular_id: UUID
    referencia: str
    valor_total: Decimal
    data_emissao: date
    data_vencimento: date
    version: int = 1
    event_name = 'FaturaEmitida'

    @classmethod
    def from_fatura(cls, item: FaturaAgua) -> 'FaturaEmitidaEvent':
        return cls(event_id=uuid4(), occurred_at=datetime.now(timezone.utc), fatura_id=item.id, numero_fatura=item.numero_fatura, consumo_id=item.consumo_id, titular_id=item.titular_id, referencia=item.referencia, valor_total=item.valor_total, data_emissao=item.data_emissao, data_vencimento=item.data_vencimento)

    def to_payload(self) -> dict:
        return {'event_id': str(self.event_id), 'occurred_at': self.occurred_at.isoformat(), 'fatura_id': str(self.fatura_id), 'numero_fatura': self.numero_fatura, 'consumo_id': str(self.consumo_id), 'titular_id': str(self.titular_id), 'referencia': self.referencia, 'valor_total': str(self.valor_total), 'data_emissao': _to_iso_date(self.data_emissao), 'data_vencimento': _to_iso_date(self.data_vencimento), 'version': self.version}

    @classmethod
    def from_payload(cls, payload: dict) -> 'FaturaEmitidaEvent':
        return cls(event_id=UUID(payload['event_id']), occurred_at=datetime.fromisoformat(payload['occurred_at']), fatura_id=UUID(payload['fatura_id']), numero_fatura=payload['numero_fatura'], consumo_id=UUID(payload['consumo_id']), titular_id=UUID(payload['titular_id']), referencia=payload['referencia'], valor_total=Decimal(payload['valor_total']), data_emissao=_from_iso_date(payload['data_emissao']), data_vencimento=_from_iso_date(payload['data_vencimento']), version=int(payload.get('version', 1)))

@dataclass(frozen=True)
class FaturaPagamentoRegistradoEvent:
    event_id: UUID
    occurred_at: datetime
    fatura_id: UUID
    numero_fatura: str
    titular_id: UUID
    valor_pago: Decimal
    data_pagamento: date
    metodo_pagamento: str
    version: int = 1
    event_name = 'FaturaPagamentoRegistrado'

    @classmethod
    def from_fatura(cls, item: FaturaAgua) -> 'FaturaPagamentoRegistradoEvent':
        if item.valor_pago is None or item.data_pagamento is None or item.metodo_pagamento is None:
            raise ValueError('Fatura deve conter dados de pagamento para gerar evento')
        return cls(event_id=uuid4(), occurred_at=datetime.now(timezone.utc), fatura_id=item.id, numero_fatura=item.numero_fatura, titular_id=item.titular_id, valor_pago=item.valor_pago, data_pagamento=item.data_pagamento, metodo_pagamento=item.metodo_pagamento.value)

    def to_payload(self) -> dict:
        return {'event_id': str(self.event_id), 'occurred_at': self.occurred_at.isoformat(), 'fatura_id': str(self.fatura_id), 'numero_fatura': self.numero_fatura, 'titular_id': str(self.titular_id), 'valor_pago': str(self.valor_pago), 'data_pagamento': _to_iso_date(self.data_pagamento), 'metodo_pagamento': self.metodo_pagamento, 'version': self.version}

    @classmethod
    def from_payload(cls, payload: dict) -> 'FaturaPagamentoRegistradoEvent':
        return cls(event_id=UUID(payload['event_id']), occurred_at=datetime.fromisoformat(payload['occurred_at']), fatura_id=UUID(payload['fatura_id']), numero_fatura=payload['numero_fatura'], titular_id=UUID(payload['titular_id']), valor_pago=Decimal(payload['valor_pago']), data_pagamento=_from_iso_date(payload['data_pagamento']), metodo_pagamento=payload['metodo_pagamento'], version=int(payload.get('version', 1)))