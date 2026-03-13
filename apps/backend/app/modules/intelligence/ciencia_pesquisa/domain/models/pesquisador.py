from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from app.modules.intelligence.ciencia_pesquisa.domain.enums import AreaConhecimento, NivelFormacao, StatusVinculoPesquisador, TipoVinculoPesquisador

@dataclass
class Pesquisador:
    id: UUID
    nome_completo: str
    documento_identificacao: str
    email_institucional: str
    instituicao_id: UUID | None
    unidade_pesquisa_id: UUID | None
    area_conhecimento: AreaConhecimento
    nivel_formacao: NivelFormacao
    tipo_vinculo: TipoVinculoPesquisador
    status_vinculo: StatusVinculoPesquisador
    data_inicio_vinculo: date
    data_fim_vinculo: date | None = None
    telefone: str | None = None
    orcid: str | None = None
    lattes_url: str | None = None
    researcher_id: str | None = None
    scopus_id: str | None = None
    ativo: bool = True

    @classmethod
    def cadastrar(cls, *, nome_completo: str, documento_identificacao: str, email_institucional: str, instituicao_id: UUID | None=None, unidade_pesquisa_id: UUID | None=None, area_conhecimento: AreaConhecimento=AreaConhecimento.MULTIDISCIPLINAR, nivel_formacao: NivelFormacao=NivelFormacao.GRADUADO, tipo_vinculo: TipoVinculoPesquisador=TipoVinculoPesquisador.EFETIVO, data_inicio_vinculo: date | None=None, telefone: str | None=None, orcid: str | None=None, lattes_url: str | None=None, researcher_id: str | None=None, scopus_id: str | None=None) -> 'Pesquisador':
        nome = nome_completo.strip()
        if len(nome) < 3:
            raise ValueError('Nome do pesquisador deve ter pelo menos 3 caracteres')
        email = email_institucional.strip().lower()
        if '@' not in email:
            raise ValueError('Email institucional invalido')
        return cls(id=uuid4(), nome_completo=nome, documento_identificacao=documento_identificacao.strip(), email_institucional=email, instituicao_id=instituicao_id, unidade_pesquisa_id=unidade_pesquisa_id, area_conhecimento=area_conhecimento, nivel_formacao=nivel_formacao, tipo_vinculo=tipo_vinculo, status_vinculo=StatusVinculoPesquisador.ATIVO, data_inicio_vinculo=data_inicio_vinculo or date.today(), data_fim_vinculo=None, telefone=telefone.strip() if telefone else None, orcid=orcid.strip() if orcid else None, lattes_url=lattes_url.strip() if lattes_url else None, researcher_id=researcher_id.strip() if researcher_id else None, scopus_id=scopus_id.strip() if scopus_id else None, ativo=True)

    def atualizar_vinculo(self, *, tipo_vinculo: TipoVinculoPesquisador | None=None, status_vinculo: StatusVinculoPesquisador | None=None, unidade_pesquisa_id: UUID | None=None) -> None:
        if tipo_vinculo is not None:
            self.tipo_vinculo = tipo_vinculo
        if status_vinculo is not None:
            self.status_vinculo = status_vinculo
            self.ativo = status_vinculo in {StatusVinculoPesquisador.ATIVO, StatusVinculoPesquisador.AFASTADO}
        if unidade_pesquisa_id is not None:
            self.unidade_pesquisa_id = unidade_pesquisa_id

    def encerrar_vinculo(self, *, data_fim_vinculo: date | None=None) -> None:
        fim = data_fim_vinculo or date.today()
        if fim < self.data_inicio_vinculo:
            raise ValueError('Data de encerramento nao pode ser anterior ao inicio')
        self.data_fim_vinculo = fim
        self.status_vinculo = StatusVinculoPesquisador.ENCERRADO
        self.ativo = False