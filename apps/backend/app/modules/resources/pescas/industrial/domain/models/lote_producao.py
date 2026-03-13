from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.resources.pescas.industrial.domain.enums import MercadoDestino, StatusLoteProducao

@dataclass
class LoteProducao:
    id: UUID
    codigo_lote: str
    unidade_processamento_id: UUID
    produto_processado_id: UUID
    data_producao: date
    quantidade_kg: Decimal
    status: StatusLoteProducao
    destino_mercado: MercadoDestino
    data_validade: date | None = None
    turno: str | None = None
    temperatura_armazenamento_c: Decimal | None = None
    observacoes: str | None = None

    @classmethod
    def criar(cls, *, codigo_lote: str, unidade_processamento_id: UUID, produto_processado_id: UUID, data_producao: date, quantidade_kg: Decimal, destino_mercado: MercadoDestino, data_validade: date | None=None, turno: str | None=None, temperatura_armazenamento_c: Decimal | None=None, observacoes: str | None=None) -> 'LoteProducao':
        if quantidade_kg <= 0:
            raise ValueError('Quantidade deve ser maior que zero')
        if data_validade and data_validade < data_producao:
            raise ValueError('Validade nao pode ser anterior a data de producao')
        return cls(id=uuid4(), codigo_lote=codigo_lote.strip(), unidade_processamento_id=unidade_processamento_id, produto_processado_id=produto_processado_id, data_producao=data_producao, quantidade_kg=quantidade_kg, status=StatusLoteProducao.ABERTO, destino_mercado=destino_mercado, data_validade=data_validade, turno=turno.strip() if turno else None, temperatura_armazenamento_c=temperatura_armazenamento_c, observacoes=observacoes.strip() if observacoes else None)

    def atualizar(self, *, quantidade_kg: Decimal | None=None, status: StatusLoteProducao | None=None, destino_mercado: MercadoDestino | None=None, data_validade: date | None=None, turno: str | None=None, temperatura_armazenamento_c: Decimal | None=None, observacoes: str | None=None) -> None:
        if quantidade_kg is not None:
            if quantidade_kg <= 0:
                raise ValueError('Quantidade deve ser maior que zero')
            self.quantidade_kg = quantidade_kg
        if status is not None:
            self.status = status
        if destino_mercado is not None:
            self.destino_mercado = destino_mercado
        if data_validade is not None:
            if data_validade < self.data_producao:
                raise ValueError('Validade nao pode ser anterior a data de producao')
            self.data_validade = data_validade
        if turno is not None:
            self.turno = turno.strip() if turno else None
        if temperatura_armazenamento_c is not None:
            self.temperatura_armazenamento_c = temperatura_armazenamento_c
        if observacoes is not None:
            self.observacoes = observacoes.strip() if observacoes else None