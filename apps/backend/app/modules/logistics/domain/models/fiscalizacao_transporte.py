from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

@dataclass
class FiscalizacaoTransporte:
    id: UUID
    fiscal_id: UUID
    conformidade: bool
    apontamentos: str
    data_fiscalizacao: date
    auto_infracao: str | None = None
    observacoes: str | None = None

    @classmethod
    def registrar(cls, *, fiscal_id: UUID, conformidade: bool, apontamentos: str, data_fiscalizacao: date | None=None, auto_infracao: str | None=None, observacoes: str | None=None) -> 'FiscalizacaoTransporte':
        if not apontamentos.strip():
            raise ValueError('Apontamentos da fiscalizacao sao obrigatorios')
        return cls(id=uuid4(), fiscal_id=fiscal_id, conformidade=conformidade, apontamentos=apontamentos.strip(), data_fiscalizacao=data_fiscalizacao or date.today(), auto_infracao=auto_infracao.strip() if auto_infracao else None, observacoes=observacoes.strip() if observacoes else None)

    def to_dict(self) -> dict:
        return {'id': str(self.id), 'fiscal_id': str(self.fiscal_id), 'conformidade': self.conformidade, 'apontamentos': self.apontamentos, 'data_fiscalizacao': self.data_fiscalizacao.isoformat(), 'auto_infracao': self.auto_infracao, 'observacoes': self.observacoes}