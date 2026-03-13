from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

@dataclass
class Comercializacao:
    id: UUID
    codigo_comercializacao: str
    codigo_safra: str
    comprador: str
    quantidade_ton: float
    preco_unitario: float
    valor_total: float
    data_venda: date

    @classmethod
    def registrar(cls, *, codigo_safra: str, comprador: str, quantidade_ton: float, preco_unitario: float) -> 'Comercializacao':
        if quantidade_ton <= 0:
            raise ValueError('Quantidade vendida deve ser maior que zero')
        if preco_unitario <= 0:
            raise ValueError('Preco unitario deve ser maior que zero')
        valor_total = round(quantidade_ton * preco_unitario, 2)
        return cls(id=uuid4(), codigo_comercializacao='', codigo_safra=codigo_safra, comprador=comprador, quantidade_ton=round(quantidade_ton, 3), preco_unitario=round(preco_unitario, 2), valor_total=valor_total, data_venda=date.today())