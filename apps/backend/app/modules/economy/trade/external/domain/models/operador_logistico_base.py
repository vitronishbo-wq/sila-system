from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from app.modules.economy.trade.external.domain.enums import StatusHabilitacao, TipoOperador, TipoPessoa

@dataclass
class OperadorLogisticoBase:
    id: UUID
    cadastro_radar: str
    tipo_operador: TipoOperador
    tipo_pessoa: TipoPessoa
    status: StatusHabilitacao
    razao_social: str
    cnpj_cpf: str
    endereco: str
    numero: str
    bairro: str
    municipio: str
    provincia: str
    cep: str
    nome_fantasia: str | None = None
    complemento: str | None = None
    pais: str = 'AO'
    telefone: str | None = None
    email: str | None = None
    site: str | None = None
    numero_licenca: str | None = None
    orgao_anuente: str | None = None
    data_habilitacao: date | None = None
    data_validade: date | None = None
    data_suspensao: date | None = None
    data_cancelamento: date | None = None
    motivo_cancelamento: str | None = None
    observacoes: str | None = None

    @classmethod
    def cadastrar(cls, *, tipo_operador: TipoOperador, razao_social: str, cnpj_cpf: str, tipo_pessoa: TipoPessoa, endereco: str, numero: str, bairro: str, municipio: str, provincia: str, cep: str) -> 'OperadorLogisticoBase':
        if not razao_social.strip():
            raise ValueError('Razao social e obrigatoria')
        if not cnpj_cpf.strip():
            raise ValueError('CNPJ/CPF e obrigatorio')
        return cls(id=uuid4(), cadastro_radar='', tipo_operador=tipo_operador, tipo_pessoa=tipo_pessoa, status=StatusHabilitacao.PENDENTE, razao_social=razao_social.strip(), cnpj_cpf=cnpj_cpf.strip(), endereco=endereco.strip(), numero=numero.strip(), bairro=bairro.strip(), municipio=municipio.strip(), provincia=provincia.strip(), cep=cep.strip())

    def habilitar(self, numero_radar: str, data_habilitacao: date, data_validade: date) -> None:
        if self.status != StatusHabilitacao.PENDENTE:
            raise ValueError('Operador precisa estar pendente')
        if not numero_radar.strip():
            raise ValueError('Numero RADAR e obrigatorio')
        if data_validade < data_habilitacao:
            raise ValueError('Data de validade nao pode ser anterior a habilitacao')
        self.status = StatusHabilitacao.HABILITADO
        self.cadastro_radar = numero_radar.strip()
        self.data_habilitacao = data_habilitacao
        self.data_validade = data_validade

    def suspender(self, data_suspensao: date, motivo: str) -> None:
        if self.status != StatusHabilitacao.HABILITADO:
            raise ValueError('Apenas operadores habilitados podem ser suspensos')
        if not motivo.strip():
            raise ValueError('Motivo da suspensao e obrigatorio')
        self.status = StatusHabilitacao.SUSPENSO
        self.data_suspensao = data_suspensao
        self.observacoes = motivo.strip()

    def cancelar(self, data_cancelamento: date, motivo: str) -> None:
        if not motivo.strip():
            raise ValueError('Motivo do cancelamento e obrigatorio')
        self.status = StatusHabilitacao.CANCELADO
        self.data_cancelamento = data_cancelamento
        self.motivo_cancelamento = motivo.strip()

    def reabilitar(self) -> None:
        if self.status != StatusHabilitacao.SUSPENSO:
            raise ValueError('Apenas operadores suspensos podem ser reabilitados')
        self.status = StatusHabilitacao.HABILITADO