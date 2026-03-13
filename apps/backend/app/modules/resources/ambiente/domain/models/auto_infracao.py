from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.resources.ambiente.domain.enums import StatusAutoInfracao, TipoAutoInfracao

@dataclass
class AutoInfracao:
    id: UUID
    numero_auto: str
    numero_fiscalizacao: str
    tipo: TipoAutoInfracao
    descricao: str
    fiscal_id: UUID
    status: StatusAutoInfracao
    data_lavratura: date
    valor_multa: Decimal | None = None
    observacoes: str | None = None

    @classmethod
    def lavrar(cls, *, numero_fiscalizacao: str, tipo: TipoAutoInfracao, descricao: str, fiscal_id: UUID, valor_multa: Decimal | None=None) -> 'AutoInfracao':
        if not descricao.strip():
            raise ValueError('Descricao do auto de infracao e obrigatoria')
        if tipo == TipoAutoInfracao.MULTA:
            if valor_multa is None or valor_multa <= Decimal('0'):
                raise ValueError('Valor da multa deve ser maior que zero para tipo multa')
        return cls(id=uuid4(), numero_auto='', numero_fiscalizacao=numero_fiscalizacao, tipo=tipo, descricao=descricao.strip(), fiscal_id=fiscal_id, status=StatusAutoInfracao.LAVRADO, data_lavratura=date.today(), valor_multa=valor_multa.quantize(Decimal('0.01')) if valor_multa is not None else None)

    def notificar(self) -> None:
        if self.status != StatusAutoInfracao.LAVRADO:
            raise ValueError('Apenas auto lavrado pode ser notificado')
        self.status = StatusAutoInfracao.NOTIFICADO

    def registrar_recurso(self) -> None:
        if self.status != StatusAutoInfracao.NOTIFICADO:
            raise ValueError('Apenas auto notificado pode entrar em recurso')
        self.status = StatusAutoInfracao.EM_RECURSO

    def julgar(self, *, mantido: bool, observacoes: str | None=None) -> None:
        if self.status not in {StatusAutoInfracao.NOTIFICADO, StatusAutoInfracao.EM_RECURSO}:
            raise ValueError('Auto de infracao nao esta apto para julgamento')
        self.status = StatusAutoInfracao.JULGADO if mantido else StatusAutoInfracao.CANCELADO
        self.observacoes = observacoes.strip() if observacoes else None