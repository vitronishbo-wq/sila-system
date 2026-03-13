from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from app.modules.society.desporto.domain.enums import StatusContrato, TipoContrato

@dataclass
class Contrato:
    id: UUID
    codigo_contrato: str
    atleta_id: UUID
    clube_id: UUID
    tipo: TipoContrato
    data_inicio: date
    data_fim: date
    salario_mensal: Decimal
    status: StatusContrato
    clausula_rescisao: Decimal | None = None
    ativo: bool = True
    observacoes: str | None = None

    @classmethod
    def assinar(cls, *, codigo_contrato: str, atleta_id: UUID, clube_id: UUID, tipo: TipoContrato, data_inicio: date, data_fim: date, salario_mensal: Decimal, clausula_rescisao: Decimal | None=None, observacoes: str | None=None) -> 'Contrato':
        if data_fim < data_inicio:
            raise ValueError('Data de fim deve ser maior ou igual a data de inicio')
        if salario_mensal <= 0:
            raise ValueError('Salario mensal deve ser positivo')
        if clausula_rescisao is not None and clausula_rescisao <= 0:
            raise ValueError('Clausula de rescisao deve ser positiva')
        return cls(id=uuid4(), codigo_contrato=codigo_contrato.strip(), atleta_id=atleta_id, clube_id=clube_id, tipo=tipo, data_inicio=data_inicio, data_fim=data_fim, salario_mensal=salario_mensal, clausula_rescisao=clausula_rescisao, status=StatusContrato.ATIVO, observacoes=observacoes.strip() if observacoes else None)

    def encerrar(self, *, observacoes: str | None=None) -> None:
        self.status = StatusContrato.ENCERRADO
        self.ativo = False
        if observacoes:
            self.observacoes = observacoes.strip()

    def rescindir(self, *, motivo: str | None=None) -> None:
        self.status = StatusContrato.RESCINDIDO
        self.ativo = False
        if motivo:
            self.observacoes = motivo.strip()