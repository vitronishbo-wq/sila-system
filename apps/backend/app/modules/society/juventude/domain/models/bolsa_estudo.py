from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from app.modules.society.juventude.domain.enums import TipoBolsa

@dataclass
class BolsaEstudo:
    id: UUID
    codigo_bolsa: str
    jovem_id: UUID
    tipo: TipoBolsa
    valor_mensal: Decimal
    data_inicio: date
    data_cadastro: date
    data_fim: date | None = None
    observacoes: str | None = None
    ativa: bool = True

    @classmethod
    def conceder(cls, *, codigo_bolsa: str, jovem_id: UUID, tipo: TipoBolsa, valor_mensal: Decimal, data_inicio: date, data_fim: date | None=None, observacoes: str | None=None) -> 'BolsaEstudo':
        if valor_mensal <= 0:
            raise ValueError('Valor mensal da bolsa deve ser maior que zero')
        if data_fim is not None and data_fim < data_inicio:
            raise ValueError('Data fim da bolsa deve ser maior ou igual a data inicio')
        return cls(id=uuid4(), codigo_bolsa=codigo_bolsa.strip(), jovem_id=jovem_id, tipo=tipo, valor_mensal=valor_mensal, data_inicio=data_inicio, data_fim=data_fim, data_cadastro=date.today(), observacoes=observacoes.strip() if observacoes else None, ativa=True)

    def encerrar(self, observacoes: str | None=None) -> None:
        self.ativa = False
        self.data_fim = date.today()
        if observacoes is not None:
            self.observacoes = observacoes.strip() or None