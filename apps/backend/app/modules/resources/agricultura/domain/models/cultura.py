from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from app.modules.resources.agricultura.domain.enums import TipoCultura

@dataclass
class Cultura:
    id: UUID
    codigo_cultura: str
    nome: str
    tipo: TipoCultura
    ciclo_dias: int
    produtividade_estimada_ton_ha: float
    data_registro: date
    ativa: bool = True

    @classmethod
    def criar(cls, *, nome: str, tipo: TipoCultura, ciclo_dias: int, produtividade_estimada_ton_ha: float) -> 'Cultura':
        if ciclo_dias <= 0:
            raise ValueError('Ciclo em dias deve ser maior que zero')
        if produtividade_estimada_ton_ha < 0:
            raise ValueError('Produtividade estimada nao pode ser negativa')
        return cls(id=uuid4(), codigo_cultura='', nome=nome, tipo=tipo, ciclo_dias=ciclo_dias, produtividade_estimada_ton_ha=round(produtividade_estimada_ton_ha, 2), data_registro=date.today(), ativa=True)