from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from app.modules.society.assistencia_social.domain.enums import FaixaVulnerabilidade, SituacaoBeneficiario

@dataclass
class Beneficiario:
    id: UUID
    numero_registro: str
    citizen_id: UUID
    cadastro_unico_id: UUID | None
    faixa_vulnerabilidade: FaixaVulnerabilidade
    situacao: SituacaoBeneficiario
    data_cadastro: date
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def cadastrar(cls, *, numero_registro: str, citizen_id: UUID, cadastro_unico_id: UUID | None, faixa_vulnerabilidade: FaixaVulnerabilidade, observacoes: str | None=None) -> 'Beneficiario':
        return cls(id=uuid4(), numero_registro=numero_registro, citizen_id=citizen_id, cadastro_unico_id=cadastro_unico_id, faixa_vulnerabilidade=faixa_vulnerabilidade, situacao=SituacaoBeneficiario.ATIVO, data_cadastro=date.today(), observacoes=observacoes, ativo=True)

    def atualizar_vulnerabilidade(self, faixa: FaixaVulnerabilidade) -> None:
        self.faixa_vulnerabilidade = faixa

    def suspender(self, motivo: str | None=None) -> None:
        self.situacao = SituacaoBeneficiario.SUSPENSO
        self.ativo = False
        if motivo:
            self.observacoes = motivo

    def inativar(self, motivo: str | None=None) -> None:
        self.situacao = SituacaoBeneficiario.INATIVO
        self.ativo = False
        if motivo:
            self.observacoes = motivo