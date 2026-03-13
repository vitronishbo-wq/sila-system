from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

@dataclass
class FiscalizacaoObra:
    id: UUID
    data_fiscalizacao: date
    fiscal_id: UUID
    conformidade: bool
    apontamentos: str
    recomendacoes: str | None = None

    @classmethod
    def registrar(cls, *, fiscal_id: UUID, conformidade: bool, apontamentos: str, recomendacoes: str | None=None, data_fiscalizacao: date | None=None) -> 'FiscalizacaoObra':
        if not apontamentos.strip():
            raise ValueError('Apontamentos da fiscalizacao sao obrigatorios')
        return cls(id=uuid4(), data_fiscalizacao=data_fiscalizacao or date.today(), fiscal_id=fiscal_id, conformidade=conformidade, apontamentos=apontamentos.strip(), recomendacoes=recomendacoes.strip() if recomendacoes else None)

    def to_dict(self) -> dict:
        return {'id': str(self.id), 'data_fiscalizacao': self.data_fiscalizacao.isoformat(), 'fiscal_id': str(self.fiscal_id), 'conformidade': self.conformidade, 'apontamentos': self.apontamentos, 'recomendacoes': self.recomendacoes}