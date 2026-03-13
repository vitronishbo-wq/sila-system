from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from apps.backend.app.modules.intelligence.ciencia_pesquisa.domain.enums import NaturezaJuridicaInstituicao, StatusCredenciamentoInstituicao, TipoInstituicaoPesquisa

@dataclass
class InstituicaoPesquisa:
    id: UUID
    sigla: str
    nome: str
    nif: str
    tipo: TipoInstituicaoPesquisa
    natureza_juridica: NaturezaJuridicaInstituicao
    pais: str
    provincia: str
    municipio: str
    endereco: str
    email_institucional: str
    telefone: str | None = None
    website: str | None = None
    status_credenciamento: StatusCredenciamentoInstituicao = StatusCredenciamentoInstituicao.EM_ANALISE
    data_credenciamento: date | None = None
    data_validade_credenciamento: date | None = None
    comite_etica_ativo: bool = False
    nucleo_inovacao_ativo: bool = False
    ativa: bool = True

    @classmethod
    def cadastrar(cls, *, sigla: str, nome: str, nif: str, tipo: TipoInstituicaoPesquisa, natureza_juridica: NaturezaJuridicaInstituicao, pais: str, provincia: str, municipio: str, endereco: str, email_institucional: str, telefone: str | None=None, website: str | None=None) -> 'InstituicaoPesquisa':
        if len(sigla.strip()) < 2:
            raise ValueError('Sigla da instituicao deve ter pelo menos 2 caracteres')
        if len(nome.strip()) < 3:
            raise ValueError('Nome da instituicao deve ter pelo menos 3 caracteres')
        email = email_institucional.strip().lower()
        if '@' not in email:
            raise ValueError('Email institucional invalido')
        return cls(id=uuid4(), sigla=sigla.strip().upper(), nome=nome.strip(), nif=nif.strip(), tipo=tipo, natureza_juridica=natureza_juridica, pais=pais.strip(), provincia=provincia.strip(), municipio=municipio.strip(), endereco=endereco.strip(), email_institucional=email, telefone=telefone.strip() if telefone else None, website=website.strip() if website else None, status_credenciamento=StatusCredenciamentoInstituicao.EM_ANALISE, ativa=True)

    def credenciar(self, *, data_credenciamento: date | None=None, data_validade_credenciamento: date | None=None) -> None:
        inicio = data_credenciamento or date.today()
        if data_validade_credenciamento and data_validade_credenciamento < inicio:
            raise ValueError('Validade do credenciamento nao pode ser anterior ao inicio')
        self.status_credenciamento = StatusCredenciamentoInstituicao.CREDENCIADA
        self.data_credenciamento = inicio
        self.data_validade_credenciamento = data_validade_credenciamento
        self.ativa = True

    def suspender(self) -> None:
        self.status_credenciamento = StatusCredenciamentoInstituicao.SUSPENSA
        self.ativa = False

    def descredenciar(self) -> None:
        self.status_credenciamento = StatusCredenciamentoInstituicao.DESCREDENCIADA
        self.ativa = False