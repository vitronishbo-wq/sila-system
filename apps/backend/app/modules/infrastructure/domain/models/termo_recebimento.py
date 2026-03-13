from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

@dataclass
class TermoRecebimento:
    id: UUID
    tipo: str
    responsavel_id: UUID
    data_termo: date
    observacoes: str | None = None

    @classmethod
    def registrar(cls, *, tipo: str, responsavel_id: UUID, data_termo: date | None=None, observacoes: str | None=None) -> 'TermoRecebimento':
        tipo_norm = tipo.strip().lower()
        if tipo_norm not in {'provisorio', 'definitivo'}:
            raise ValueError("Tipo de termo deve ser 'provisorio' ou 'definitivo'")
        return cls(id=uuid4(), tipo=tipo_norm, responsavel_id=responsavel_id, data_termo=data_termo or date.today(), observacoes=observacoes.strip() if observacoes else None)

    def to_dict(self) -> dict:
        return {'id': str(self.id), 'tipo': self.tipo, 'responsavel_id': str(self.responsavel_id), 'data_termo': self.data_termo.isoformat(), 'observacoes': self.observacoes}