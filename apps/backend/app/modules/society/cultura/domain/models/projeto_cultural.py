from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from app.modules.society.cultura.domain.enums import NaturezaProjetoCultural, StatusProjetoCultural, TipoProjetoCultural

@dataclass
class ProjetoCultural:
    id: UUID
    codigo_projeto: str
    titulo: str
    tipo: TipoProjetoCultural
    natureza: NaturezaProjetoCultural
    proponente_cpf_cnpj: str
    proponente_nome: str
    resumo: str
    valor_solicitado: Decimal
    data_submissao: date
    status: StatusProjetoCultural = StatusProjetoCultural.RASCUNHO
    justificativa: str | None = None
    edital_id: UUID | None = None
    valor_aprovado: Decimal | None = None
    data_inicio: date | None = None
    data_fim: date | None = None
    ativo: bool = True
    objetivos: list[str] = field(default_factory=list)
    observacoes: str | None = None

    @classmethod
    def cadastrar(cls, *, codigo_projeto: str, titulo: str, tipo: TipoProjetoCultural, natureza: NaturezaProjetoCultural, proponente_cpf_cnpj: str, proponente_nome: str, resumo: str, valor_solicitado: Decimal, justificativa: str | None=None, edital_id: UUID | None=None, objetivos: list[str] | None=None, observacoes: str | None=None) -> 'ProjetoCultural':
        if len(titulo.strip()) < 5:
            raise ValueError('Titulo do projeto deve ter pelo menos 5 caracteres')
        if valor_solicitado <= 0:
            raise ValueError('Valor solicitado deve ser positivo')
        return cls(id=uuid4(), codigo_projeto=codigo_projeto.strip(), titulo=titulo.strip(), tipo=tipo, natureza=natureza, proponente_cpf_cnpj=proponente_cpf_cnpj.strip(), proponente_nome=proponente_nome.strip(), resumo=resumo.strip(), valor_solicitado=valor_solicitado, data_submissao=date.today(), justificativa=justificativa.strip() if justificativa else None, edital_id=edital_id, objetivos=[item.strip() for item in objetivos or [] if item and item.strip()], observacoes=observacoes.strip() if observacoes else None)

    def submeter(self) -> None:
        if self.status == StatusProjetoCultural.RASCUNHO:
            self.status = StatusProjetoCultural.SUBMETIDO

    def aprovar(self, *, valor_aprovado: Decimal) -> None:
        if valor_aprovado <= 0:
            raise ValueError('Valor aprovado deve ser positivo')
        self.valor_aprovado = valor_aprovado
        self.status = StatusProjetoCultural.APROVADO

    def reprovar(self) -> None:
        self.status = StatusProjetoCultural.REPROVADO

    def iniciar_execucao(self, *, data_inicio: date) -> None:
        self.data_inicio = data_inicio
        self.status = StatusProjetoCultural.EM_EXECUCAO

    def concluir(self, *, data_fim: date) -> None:
        if self.data_inicio and data_fim < self.data_inicio:
            raise ValueError('Data fim nao pode ser anterior a data inicio')
        self.data_fim = data_fim
        self.status = StatusProjetoCultural.CONCLUIDO

    def atualizar(self, *, titulo: str | None=None, tipo: TipoProjetoCultural | None=None, natureza: NaturezaProjetoCultural | None=None, resumo: str | None=None, valor_solicitado: Decimal | None=None, justificativa: str | None=None, objetivos: list[str] | None=None, ativo: bool | None=None, observacoes: str | None=None) -> None:
        if titulo is not None:
            titulo_normalizado = titulo.strip()
            if len(titulo_normalizado) < 5:
                raise ValueError('Titulo do projeto deve ter pelo menos 5 caracteres')
            self.titulo = titulo_normalizado
        if tipo is not None:
            self.tipo = tipo
        if natureza is not None:
            self.natureza = natureza
        if resumo is not None:
            self.resumo = resumo.strip()
        if valor_solicitado is not None:
            if valor_solicitado <= 0:
                raise ValueError('Valor solicitado deve ser positivo')
            self.valor_solicitado = valor_solicitado
        if justificativa is not None:
            self.justificativa = justificativa.strip() if justificativa else None
        if objetivos is not None:
            self.objetivos = [item.strip() for item in objetivos if item and item.strip()]
        if ativo is not None:
            self.ativo = ativo
        if observacoes is not None:
            self.observacoes = observacoes.strip() if observacoes else None