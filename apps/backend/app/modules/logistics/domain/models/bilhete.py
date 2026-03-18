from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.logistics.domain.enums import TipoTarifa

def _percentual_desconto(tipo_tarifa: TipoTarifa) -> Decimal:
    if tipo_tarifa == TipoTarifa.ESTUDANTE:
        return Decimal('0.50')
    if tipo_tarifa in {TipoTarifa.IDOSO, TipoTarifa.PCD}:
        return Decimal('1.00')
    if tipo_tarifa == TipoTarifa.VALE_TRANSPORTE:
        return Decimal('0.10')
    return Decimal('0.00')

@dataclass
class Bilhete:
    id: UUID
    codigo_bilhete: str
    viagem_id: UUID
    tipo_tarifa: TipoTarifa
    valor_pago: Decimal
    valor_integral: Decimal
    forma_pagamento: str
    data_hora_emissao: datetime
    passageiro_id: UUID | None = None
    passageiro_nome: str | None = None
    passageiro_documento: str | None = None
    desconto: Decimal | None = None
    data_hora_embarque: datetime | None = None
    embarque_realizado: bool = False
    assento: str | None = None
    observacoes: str | None = None

    @classmethod
    def emitir(cls, *, viagem_id: UUID, tipo_tarifa: TipoTarifa, valor_integral: Decimal, forma_pagamento: str, passageiro_id: UUID | None=None, passageiro_nome: str | None=None, passageiro_documento: str | None=None, assento: str | None=None, observacoes: str | None=None) -> 'Bilhete':
        if valor_integral <= Decimal('0'):
            raise ValueError('Valor integral do bilhete deve ser maior que zero')
        if not forma_pagamento.strip():
            raise ValueError('Forma de pagamento do bilhete e obrigatoria')
        percentual = _percentual_desconto(tipo_tarifa)
        desconto = (valor_integral * percentual).quantize(Decimal('0.01'))
        valor_pago = (valor_integral - desconto).quantize(Decimal('0.01'))
        codigo = f'BLT-{datetime.utcnow():%Y%m%d%H%M%S}-{uuid4().hex[:6].upper()}'
        return cls(id=uuid4(), codigo_bilhete=codigo, viagem_id=viagem_id, tipo_tarifa=tipo_tarifa, valor_pago=valor_pago, valor_integral=valor_integral.quantize(Decimal('0.01')), forma_pagamento=forma_pagamento.strip().lower(), data_hora_emissao=datetime.utcnow(), passageiro_id=passageiro_id, passageiro_nome=passageiro_nome.strip() if passageiro_nome else None, passageiro_documento=passageiro_documento.strip() if passageiro_documento else None, desconto=desconto, assento=assento.strip().upper() if assento else None, observacoes=observacoes.strip() if observacoes else None)

    def registrar_embarque(self, data_hora_embarque: datetime | None=None) -> None:
        self.data_hora_embarque = data_hora_embarque or datetime.utcnow()
        self.embarque_realizado = True