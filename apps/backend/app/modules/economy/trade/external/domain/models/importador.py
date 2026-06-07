from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from apps.backend.app.modules.economy.trade.external.domain.enums import (
    RegimeImportacao,
    StatusHabilitacao,
    TipoOperador,
    TipoPessoa,
)


@dataclass
class Importador:
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
    regimes_autorizados: list[RegimeImportacao]
    nome_fantasia: str | None = None
    inscricao_estadual: str | None = None
    inscricao_municipal: str | None = None
    complemento: str | None = None
    pais: str = "AO"
    telefone: str | None = None
    email: str | None = None
    site: str | None = None
    representante_nome: str | None = None
    representante_cpf: str | None = None
    representante_cargo: str | None = None
    responsavel_nome: str | None = None
    responsavel_cpf: str | None = None
    responsavel_registro: str | None = None
    data_habilitacao: date | None = None
    data_validade: date | None = None
    data_suspensao: date | None = None
    data_cancelamento: date | None = None
    motivo_cancelamento: str | None = None
    produtos_principais: list[str] | None = None
    paises_origem: list[str] | None = None
    banco_principal: str | None = None
    conta_corrente: str | None = None
    swift_code: str | None = None
    limite_credito: Decimal | None = None
    observacoes: str | None = None

    @classmethod
    def cadastrar(
        cls,
        *,
        razao_social: str,
        cnpj_cpf: str,
        tipo_pessoa: TipoPessoa,
        endereco: str,
        numero: str,
        bairro: str,
        municipio: str,
        provincia: str,
        cep: str,
        regimes_autorizados: list[RegimeImportacao],
    ) -> Importador:
        if not razao_social.strip():
            raise ValueError("Razao social e obrigatoria")
        if not cnpj_cpf.strip():
            raise ValueError("CNPJ/CPF e obrigatorio")
        if not regimes_autorizados:
            raise ValueError("Ao menos um regime de importacao deve ser informado")
        return cls(
            id=uuid4(),
            cadastro_radar="",
            tipo_operador=TipoOperador.IMPORTADOR,
            tipo_pessoa=tipo_pessoa,
            status=StatusHabilitacao.PENDENTE,
            razao_social=razao_social.strip(),
            cnpj_cpf=cnpj_cpf.strip(),
            endereco=endereco.strip(),
            numero=numero.strip(),
            bairro=bairro.strip(),
            municipio=municipio.strip(),
            provincia=provincia.strip(),
            cep=cep.strip(),
            regimes_autorizados=list(regimes_autorizados),
        )

    def habilitar(self, numero_radar: str, data_habilitacao: date, data_validade: date) -> None:
        if self.status != StatusHabilitacao.PENDENTE:
            raise ValueError("Importador precisa estar pendente")
        if not numero_radar.strip():
            raise ValueError("Numero RADAR e obrigatorio")
        if data_validade < data_habilitacao:
            raise ValueError("Data de validade nao pode ser anterior a habilitacao")
        self.status = StatusHabilitacao.HABILITADO
        self.cadastro_radar = numero_radar.strip()
        self.data_habilitacao = data_habilitacao
        self.data_validade = data_validade

    def suspender(self, data_suspensao: date, motivo: str) -> None:
        if self.status != StatusHabilitacao.HABILITADO:
            raise ValueError("Apenas importadores habilitados podem ser suspensos")
        if not motivo.strip():
            raise ValueError("Motivo da suspensao e obrigatorio")
        self.status = StatusHabilitacao.SUSPENSO
        self.data_suspensao = data_suspensao
        self.observacoes = motivo.strip()

    def cancelar(self, data_cancelamento: date, motivo: str) -> None:
        if not motivo.strip():
            raise ValueError("Motivo do cancelamento e obrigatorio")
        self.status = StatusHabilitacao.CANCELADO
        self.data_cancelamento = data_cancelamento
        self.motivo_cancelamento = motivo.strip()

    def reabilitar(self) -> None:
        if self.status != StatusHabilitacao.SUSPENSO:
            raise ValueError("Apenas importadores suspensos podem ser reabilitados")
        self.status = StatusHabilitacao.HABILITADO

    def adicionar_produto(self, produto: str) -> None:
        nome = produto.strip()
        if not nome:
            raise ValueError("Produto deve ser informado")
        if self.produtos_principais is None:
            self.produtos_principais = []
        if nome not in self.produtos_principais:
            self.produtos_principais.append(nome)

    def adicionar_pais_origem(self, pais: str) -> None:
        codigo = pais.strip().upper()
        if not codigo:
            raise ValueError("Pais origem deve ser informado")
        if self.paises_origem is None:
            self.paises_origem = []
        if codigo not in self.paises_origem:
            self.paises_origem.append(codigo)
