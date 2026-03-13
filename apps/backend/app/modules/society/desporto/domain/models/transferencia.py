from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from app.modules.society.desporto.domain.enums import StatusTransferencia

@dataclass
class Transferencia:
    id: UUID
    codigo_transferencia: str
    atleta_id: UUID
    clube_origem_id: UUID
    clube_destino_id: UUID
    data_solicitacao: date
    status: StatusTransferencia
    data_conclusao: date | None = None
    valor_transferencia: Decimal | None = None
    ativo: bool = True
    observacoes: str | None = None

    @classmethod
    def solicitar(cls, *, codigo_transferencia: str, atleta_id: UUID, clube_origem_id: UUID, clube_destino_id: UUID, valor_transferencia: Decimal | None=None, observacoes: str | None=None) -> 'Transferencia':
        if clube_origem_id == clube_destino_id:
            raise ValueError('Clube origem e destino devem ser diferentes')
        if valor_transferencia is not None and valor_transferencia <= 0:
            raise ValueError('Valor de transferencia deve ser positivo')
        return cls(id=uuid4(), codigo_transferencia=codigo_transferencia.strip(), atleta_id=atleta_id, clube_origem_id=clube_origem_id, clube_destino_id=clube_destino_id, data_solicitacao=date.today(), status=StatusTransferencia.EM_NEGOCIACAO, valor_transferencia=valor_transferencia, observacoes=observacoes.strip() if observacoes else None)

    def aprovar(self) -> None:
        if self.status not in {StatusTransferencia.EM_NEGOCIACAO, StatusTransferencia.REJEITADA}:
            raise ValueError('Transferencia nao pode ser aprovada no estado atual')
        self.status = StatusTransferencia.APROVADA

    def rejeitar(self, *, motivo: str | None=None) -> None:
        if self.status not in {StatusTransferencia.EM_NEGOCIACAO, StatusTransferencia.APROVADA}:
            raise ValueError('Transferencia nao pode ser rejeitada no estado atual')
        self.status = StatusTransferencia.REJEITADA
        if motivo:
            self.observacoes = motivo.strip()

    def concluir(self) -> None:
        if self.status != StatusTransferencia.APROVADA:
            raise ValueError('Transferencia deve estar aprovada para conclusao')
        self.status = StatusTransferencia.CONCLUIDA
        self.data_conclusao = date.today()

    def cancelar(self, *, motivo: str | None=None) -> None:
        if self.status == StatusTransferencia.CONCLUIDA:
            raise ValueError('Transferencia concluida nao pode ser cancelada')
        self.status = StatusTransferencia.CANCELADA
        if motivo:
            self.observacoes = motivo.strip()