from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import (
    StatusOneracao,
    TipoOneracao,
)


@dataclass
class Oneracao:
    id: UUID
    numero_oneracao: str
    imovel_inscricao: str
    tipo: TipoOneracao
    credor_nome: str
    valor: Decimal
    data_registro: date
    status: StatusOneracao = StatusOneracao.ATIVA
    ativo: bool = True
    documento_credor: str | None = None
    moeda: str = "AOA"
    data_vencimento: date | None = None
    descricao: str | None = None
    data_atualizacao: date | None = None
    observacoes: str | None = None

    @classmethod
    def registrar(
        cls,
        *,
        numero_oneracao: str,
        imovel_inscricao: str,
        tipo: TipoOneracao,
        credor_nome: str,
        valor: Decimal,
        documento_credor: str | None = None,
        data_vencimento: date | None = None,
        descricao: str | None = None,
    ) -> Oneracao:
        if not numero_oneracao.strip():
            raise ValueError("Numero da oneracao e obrigatorio")
        if not imovel_inscricao.strip():
            raise ValueError("Inscricao do imovel e obrigatoria")
        if not credor_nome.strip():
            raise ValueError("Nome do credor e obrigatorio")
        if valor <= Decimal("0"):
            raise ValueError("Valor da oneracao deve ser maior que zero")
        if data_vencimento and data_vencimento < date.today():
            raise ValueError("Data de vencimento nao pode estar no passado")
        return cls(
            id=uuid4(),
            numero_oneracao=numero_oneracao.strip(),
            imovel_inscricao=imovel_inscricao.strip(),
            tipo=tipo,
            credor_nome=credor_nome.strip(),
            valor=valor.quantize(Decimal("0.01")),
            data_registro=date.today(),
            documento_credor=documento_credor.strip() if documento_credor else None,
            data_vencimento=data_vencimento,
            descricao=descricao.strip() if descricao else None,
            status=StatusOneracao.ATIVA,
            ativo=True,
        )

    def atualizar_valor(self, valor: Decimal) -> None:
        if valor <= Decimal("0"):
            raise ValueError("Valor da oneracao deve ser maior que zero")
        if self.status != StatusOneracao.ATIVA:
            raise ValueError("So e permitido atualizar valor de oneracao ativa")
        self.valor = valor.quantize(Decimal("0.01"))
        self.data_atualizacao = date.today()

    def baixar(self, motivo: str) -> None:
        if not motivo.strip():
            raise ValueError("Motivo da baixa e obrigatorio")
        if self.status != StatusOneracao.ATIVA:
            raise ValueError("Apenas oneracao ativa pode ser baixada")
        self.status = StatusOneracao.BAIXADA
        self.ativo = False
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()

    def cancelar(self, motivo: str) -> None:
        if not motivo.strip():
            raise ValueError("Motivo do cancelamento e obrigatorio")
        if self.status == StatusOneracao.BAIXADA:
            raise ValueError("Oneracao baixada nao pode ser cancelada")
        self.status = StatusOneracao.CANCELADA
        self.ativo = False
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()
