from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

@dataclass
class Manutencao:
    id: UUID
    veiculo_id: UUID
    tipo: str
    oficina: str
    custo: Decimal
    data_manutencao: date
    observacoes: str | None = None

    @classmethod
    def registrar(cls, *, veiculo_id: UUID, tipo: str, oficina: str, custo: Decimal, data_manutencao: date | None=None, observacoes: str | None=None) -> 'Manutencao':
        if not tipo.strip():
            raise ValueError('Tipo de manutencao e obrigatorio')
        if not oficina.strip():
            raise ValueError('Oficina e obrigatoria')
        if custo <= Decimal('0'):
            raise ValueError('Custo de manutencao deve ser maior que zero')
        return cls(id=uuid4(), veiculo_id=veiculo_id, tipo=tipo.strip(), oficina=oficina.strip(), custo=custo.quantize(Decimal('0.01')), data_manutencao=data_manutencao or date.today(), observacoes=observacoes.strip() if observacoes else None)

    def to_dict(self) -> dict:
        return {'id': str(self.id), 'veiculo_id': str(self.veiculo_id), 'tipo': self.tipo, 'oficina': self.oficina, 'custo': str(self.custo), 'data_manutencao': self.data_manutencao.isoformat(), 'observacoes': self.observacoes}