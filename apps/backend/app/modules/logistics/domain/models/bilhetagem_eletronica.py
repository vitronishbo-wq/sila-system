from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.logistics.domain.enums import StatusReconciliacaoFinanceira, TipoTarifa

@dataclass
class BilhetagemEletronica:
    id: UUID
    codigo_bilhete: str
    viagem_id: UUID
    tipo_tarifa: TipoTarifa
    valor_pago: Decimal
    forma_pagamento: str
    data_evento: datetime
    status_reconciliacao: StatusReconciliacaoFinanceira
    lancamento_financeiro_id: str | None = None
    referencia_externa: str | None = None
    metadata: dict = field(default_factory=dict)

    @classmethod
    def registrar_evento(cls, *, codigo_bilhete: str, viagem_id: UUID, tipo_tarifa: TipoTarifa, valor_pago: Decimal, forma_pagamento: str, metadata: dict | None=None) -> 'BilhetagemEletronica':
        if not codigo_bilhete.strip():
            raise ValueError('Codigo do bilhete e obrigatorio')
        if valor_pago <= Decimal('0'):
            raise ValueError('Valor pago do bilhete deve ser maior que zero')
        if not forma_pagamento.strip():
            raise ValueError('Forma de pagamento e obrigatoria')
        return cls(id=uuid4(), codigo_bilhete=codigo_bilhete.strip(), viagem_id=viagem_id, tipo_tarifa=tipo_tarifa, valor_pago=valor_pago.quantize(Decimal('0.01')), forma_pagamento=forma_pagamento.strip().lower(), data_evento=datetime.utcnow(), status_reconciliacao=StatusReconciliacaoFinanceira.PENDENTE, metadata=metadata or {})

    def vincular_lancamento(self, lancamento_financeiro_id: str) -> None:
        self.lancamento_financeiro_id = lancamento_financeiro_id

    def confirmar_reconciliacao(self, referencia_externa: str | None=None) -> None:
        self.status_reconciliacao = StatusReconciliacaoFinanceira.CONFIRMADO
        self.referencia_externa = referencia_externa

    def rejeitar_reconciliacao(self, referencia_externa: str | None=None) -> None:
        self.status_reconciliacao = StatusReconciliacaoFinanceira.REJEITADO
        self.referencia_externa = referencia_externa