from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusCertificacao

@dataclass
class Certificacao:
    id: UUID
    codigo_certificacao: str
    codigo_propriedade: str
    tipo: str
    orgao_emissor: str
    status: StatusCertificacao
    data_solicitacao: date
    data_emissao: date | None = None
    data_validade: date | None = None
    motivo_reprovacao: str | None = None

    @classmethod
    def solicitar(cls, *, codigo_propriedade: str, tipo: str, orgao_emissor: str) -> 'Certificacao':
        return cls(id=uuid4(), codigo_certificacao='', codigo_propriedade=codigo_propriedade, tipo=tipo, orgao_emissor=orgao_emissor, status=StatusCertificacao.SOLICITADA, data_solicitacao=date.today())

    def aprovar(self, *, data_validade: date | None=None) -> None:
        if self.status != StatusCertificacao.SOLICITADA:
            raise ValueError('Somente certificacao solicitada pode ser aprovada')
        self.status = StatusCertificacao.APROVADA
        self.data_emissao = date.today()
        self.data_validade = data_validade

    def reprovar(self, motivo: str) -> None:
        if self.status != StatusCertificacao.SOLICITADA:
            raise ValueError('Somente certificacao solicitada pode ser reprovada')
        self.status = StatusCertificacao.REPROVADA
        self.motivo_reprovacao = motivo