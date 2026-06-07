from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.resources.agricultura.domain.enums import TipoInsumo


@dataclass
class Insumo:
    id: UUID
    codigo_insumo: str
    nome: str
    tipo: TipoInsumo
    unidade_medida: str
    quantidade_estoque: float
    custo_unitario: float
    data_registro: date
    ativo: bool = True

    @classmethod
    def criar(
        cls,
        *,
        nome: str,
        tipo: TipoInsumo,
        unidade_medida: str,
        quantidade_inicial: float,
        custo_unitario: float,
    ) -> Insumo:
        if quantidade_inicial < 0:
            raise ValueError("Quantidade inicial nao pode ser negativa")
        if custo_unitario < 0:
            raise ValueError("Custo unitario nao pode ser negativo")
        return cls(
            id=uuid4(),
            codigo_insumo="",
            nome=nome,
            tipo=tipo,
            unidade_medida=unidade_medida,
            quantidade_estoque=round(quantidade_inicial, 3),
            custo_unitario=round(custo_unitario, 2),
            data_registro=date.today(),
            ativo=True,
        )

    def registrar_entrada(self, quantidade: float) -> None:
        if quantidade <= 0:
            raise ValueError("Quantidade de entrada deve ser maior que zero")
        self.quantidade_estoque = round(self.quantidade_estoque + quantidade, 3)

    def registrar_baixa(self, quantidade: float) -> None:
        if quantidade <= 0:
            raise ValueError("Quantidade de baixa deve ser maior que zero")
        if quantidade > self.quantidade_estoque:
            raise ValueError("Quantidade insuficiente em estoque")
        self.quantidade_estoque = round(self.quantidade_estoque - quantidade, 3)
