from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from apps.backend.app.modules.resources.pescas.industrial.domain.enums import (
    MercadoDestino,
    TipoProcessamento,
    TipoProdutoProcessado,
)


@dataclass
class ProdutoProcessado:
    id: UUID
    codigo_produto: str
    unidade_processamento_id: UUID
    nome_comercial: str
    tipo_produto: TipoProdutoProcessado
    tipo_processamento: TipoProcessamento
    peso_liquido_kg: Decimal
    rendimento_percentual: Decimal
    mercado_destino: MercadoDestino
    data_registro: date
    ativo: bool = True
    observacoes: str | None = None

    @classmethod
    def cadastrar(
        cls,
        *,
        codigo_produto: str,
        unidade_processamento_id: UUID,
        nome_comercial: str,
        tipo_produto: TipoProdutoProcessado,
        tipo_processamento: TipoProcessamento,
        peso_liquido_kg: Decimal,
        rendimento_percentual: Decimal,
        mercado_destino: MercadoDestino,
        observacoes: str | None = None,
    ) -> ProdutoProcessado:
        if peso_liquido_kg <= 0:
            raise ValueError("Peso liquido deve ser maior que zero")
        if rendimento_percentual <= 0 or rendimento_percentual > 100:
            raise ValueError("Rendimento deve estar entre 0 e 100")
        return cls(
            id=uuid4(),
            codigo_produto=codigo_produto.strip(),
            unidade_processamento_id=unidade_processamento_id,
            nome_comercial=nome_comercial.strip(),
            tipo_produto=tipo_produto,
            tipo_processamento=tipo_processamento,
            peso_liquido_kg=peso_liquido_kg,
            rendimento_percentual=rendimento_percentual,
            mercado_destino=mercado_destino,
            data_registro=date.today(),
            observacoes=observacoes.strip() if observacoes else None,
        )

    def atualizar(
        self,
        *,
        nome_comercial: str | None = None,
        tipo_produto: TipoProdutoProcessado | None = None,
        tipo_processamento: TipoProcessamento | None = None,
        peso_liquido_kg: Decimal | None = None,
        rendimento_percentual: Decimal | None = None,
        mercado_destino: MercadoDestino | None = None,
        ativo: bool | None = None,
        observacoes: str | None = None,
    ) -> None:
        if nome_comercial is not None:
            self.nome_comercial = nome_comercial.strip()
        if tipo_produto is not None:
            self.tipo_produto = tipo_produto
        if tipo_processamento is not None:
            self.tipo_processamento = tipo_processamento
        if peso_liquido_kg is not None:
            if peso_liquido_kg <= 0:
                raise ValueError("Peso liquido deve ser maior que zero")
            self.peso_liquido_kg = peso_liquido_kg
        if rendimento_percentual is not None:
            if rendimento_percentual <= 0 or rendimento_percentual > 100:
                raise ValueError("Rendimento deve estar entre 0 e 100")
            self.rendimento_percentual = rendimento_percentual
        if mercado_destino is not None:
            self.mercado_destino = mercado_destino
        if ativo is not None:
            self.ativo = ativo
        if observacoes is not None:
            self.observacoes = observacoes.strip() if observacoes else None

    def inativar(self) -> None:
        self.ativo = False
