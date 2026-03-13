from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from apps.backend.app.modules.economy.trade.external.domain.enums import StatusHabilitacao, TipoOperador, TipoPessoa

@dataclass
class HabilitacaoBase:
    id: UUID
    tipo_operador: TipoOperador
    tipo_pessoa: TipoPessoa
    status: StatusHabilitacao
    razao_social: str
    cnpj_cpf: str
    numero_processo: str
    data_solicitacao: date
    data_analise: date | None = None
    data_validade: date | None = None
    numero_radar: str | None = None
    motivo: str | None = None
    observacoes: str | None = None

    @classmethod
    def solicitar(cls, *, tipo_operador: TipoOperador, tipo_pessoa: TipoPessoa, razao_social: str, cnpj_cpf: str, numero_processo: str, data_solicitacao: date) -> 'HabilitacaoBase':
        if not razao_social.strip():
            raise ValueError('Razao social e obrigatoria')
        if not cnpj_cpf.strip():
            raise ValueError('CNPJ/CPF e obrigatorio')
        if not numero_processo.strip():
            raise ValueError('Numero do processo e obrigatorio')
        return cls(id=uuid4(), tipo_operador=tipo_operador, tipo_pessoa=tipo_pessoa, status=StatusHabilitacao.PENDENTE, razao_social=razao_social.strip(), cnpj_cpf=cnpj_cpf.strip(), numero_processo=numero_processo.strip(), data_solicitacao=data_solicitacao)

    def aprovar(self, *, numero_radar: str, data_analise: date, data_validade: date) -> None:
        if self.status != StatusHabilitacao.PENDENTE:
            raise ValueError('Somente habilitacoes pendentes podem ser aprovadas')
        if not numero_radar.strip():
            raise ValueError('Numero RADAR e obrigatorio')
        if data_validade < data_analise:
            raise ValueError('Data de validade nao pode ser anterior a analise')
        self.status = StatusHabilitacao.HABILITADO
        self.numero_radar = numero_radar.strip()
        self.data_analise = data_analise
        self.data_validade = data_validade
        self.motivo = None

    def rejeitar(self, *, data_analise: date, motivo: str) -> None:
        if self.status != StatusHabilitacao.PENDENTE:
            raise ValueError('Somente habilitacoes pendentes podem ser rejeitadas')
        if not motivo.strip():
            raise ValueError('Motivo da rejeicao e obrigatorio')
        self.status = StatusHabilitacao.CANCELADO
        self.data_analise = data_analise
        self.motivo = motivo.strip()

    def reabrir(self) -> None:
        if self.status != StatusHabilitacao.CANCELADO:
            raise ValueError('Somente habilitacoes canceladas podem ser reabertas')
        self.status = StatusHabilitacao.PENDENTE
        self.motivo = None