from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class ObraEventAggregate:
    obra_id: str
    codigo_obra: str = ''
    status: str = 'PROJETO'
    valor_total: Decimal = Decimal('0.00')
    valor_executado: Decimal = Decimal('0.00')

    def apply(self, event_type: str, payload: dict) -> None:
        if event_type == 'ObraCriadaEvent':
            self.codigo_obra = str(payload.get('codigo_obra') or self.codigo_obra)
            self.valor_total = Decimal(str(payload.get('valor_orcado') or self.valor_total))
            self.status = 'PROJETO'
            return
        if event_type == 'ObraIniciadaEvent':
            self.status = 'EM_EXECUCAO'
            return
        if event_type == 'MedicaoAprovadaEvent':
            self.status = 'EM_EXECUCAO'
            self.valor_executado += Decimal(str(payload.get('valor_medido') or '0.00'))
            return
        if event_type == 'AditivoAssinadoEvent':
            self.valor_total += Decimal(str(payload.get('valor_adicional') or '0.00'))
            return
        if event_type == 'ObraConcluidaEvent':
            self.status = 'CONCLUIDA'

def rehydrate_obra(obra_id: str, events: list[dict]) -> ObraEventAggregate:
    aggregate = ObraEventAggregate(obra_id=obra_id)
    for event in events:
        aggregate.apply(event_type=str(event.get('event_type') or ''), payload=dict(event.get('event_data') or {}))
    return aggregate