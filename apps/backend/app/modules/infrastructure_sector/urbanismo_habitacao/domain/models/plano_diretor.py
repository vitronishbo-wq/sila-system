from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusPlanoDiretor, TipoPlanoDiretor

@dataclass
class PlanoDiretor:
    id: UUID
    codigo_plano: str
    nome: str
    tipo: TipoPlanoDiretor
    status: StatusPlanoDiretor
    provincia: str
    ano_elaboracao: int
    orgao_responsavel_id: UUID
    municipio: str | None = None
    ano_aprovacao: int | None = None
    ano_publicacao: int | None = None
    periodo_validade_inicio: date | None = None
    periodo_validade_fim: date | None = None
    lei_aprovacao: str | None = None
    participantes_consulta: int | None = None
    audiencias_publicas: int | None = None
    documento_url: str | None = None
    mapa_url: str | None = None
    area_total_urbana: Decimal | None = None
    area_total_rural: Decimal | None = None
    populacao_estimada: int | None = None
    densidade_media: Decimal | None = None
    macrozoneamento: list[dict] | None = None
    diretrizes_gerais: str | None = None
    objetivos_estrategicos: str | None = None
    observacoes: str | None = None
    data_publicacao: date | None = None

    @classmethod
    def criar(cls, *, codigo_plano: str, nome: str, tipo: TipoPlanoDiretor, provincia: str, ano_elaboracao: int, orgao_responsavel_id: UUID, municipio: str | None=None) -> 'PlanoDiretor':
        if not codigo_plano.strip():
            raise ValueError('Codigo do plano e obrigatorio')
        if not nome.strip():
            raise ValueError('Nome do plano e obrigatorio')
        if not provincia.strip():
            raise ValueError('Provincia e obrigatoria')
        if ano_elaboracao < 1900:
            raise ValueError('Ano de elaboracao invalido')
        return cls(id=uuid4(), codigo_plano=codigo_plano.strip(), nome=nome.strip(), tipo=tipo, status=StatusPlanoDiretor.ELABORACAO, provincia=provincia.strip(), ano_elaboracao=ano_elaboracao, orgao_responsavel_id=orgao_responsavel_id, municipio=municipio.strip() if municipio else None)

    def iniciar_consulta_publica(self) -> None:
        if self.status != StatusPlanoDiretor.ELABORACAO:
            raise ValueError('Plano precisa estar em elaboracao')
        self.status = StatusPlanoDiretor.CONSULTA_PUBLICA

    def realizar_audiencia_publica(self, participantes: int) -> None:
        if self.status != StatusPlanoDiretor.CONSULTA_PUBLICA:
            raise ValueError('Plano precisa estar em consulta publica')
        if participantes <= 0:
            raise ValueError('Participantes devem ser maiores que zero')
        self.status = StatusPlanoDiretor.AUDIENCIA_PUBLICA
        self.audiencias_publicas = (self.audiencias_publicas or 0) + 1
        self.participantes_consulta = (self.participantes_consulta or 0) + participantes

    def aprovar_camara(self, *, lei: str, ano: int) -> None:
        if self.status != StatusPlanoDiretor.AUDIENCIA_PUBLICA:
            raise ValueError('Plano precisa ter passado por audiencia publica')
        if not lei.strip():
            raise ValueError('Lei de aprovacao e obrigatoria')
        if ano < self.ano_elaboracao:
            raise ValueError('Ano de aprovacao invalido')
        self.status = StatusPlanoDiretor.APROVADO_CAMARA
        self.lei_aprovacao = lei.strip()
        self.ano_aprovacao = ano

    def aprovar_prefeitura(self) -> None:
        if self.status != StatusPlanoDiretor.APROVADO_CAMARA:
            raise ValueError('Plano precisa ser aprovado pela camara')
        self.status = StatusPlanoDiretor.APROVADO_PREFEITURA

    def sancionar(self, *, data_publicacao: date) -> None:
        if self.status != StatusPlanoDiretor.APROVADO_PREFEITURA:
            raise ValueError('Plano precisa ser aprovado pela prefeitura')
        self.status = StatusPlanoDiretor.SANCIONADO
        self.data_publicacao = data_publicacao
        self.ano_publicacao = data_publicacao.year

    def publicar(self) -> None:
        if self.status != StatusPlanoDiretor.SANCIONADO:
            raise ValueError('Plano precisa ser sancionado')
        self.status = StatusPlanoDiretor.PUBLICADO

    def definir_validade(self, *, data_inicio: date, data_fim: date) -> None:
        if self.status != StatusPlanoDiretor.PUBLICADO:
            raise ValueError('Plano precisa estar publicado')
        if data_fim <= data_inicio:
            raise ValueError('Data final deve ser maior que data inicial')
        self.periodo_validade_inicio = data_inicio
        self.periodo_validade_fim = data_fim

    def atualizar_macrozoneamento(self, macrozoneamento: list[dict]) -> None:
        self.macrozoneamento = macrozoneamento

    def adicionar_diretriz(self, diretriz: str) -> None:
        if not diretriz.strip():
            raise ValueError('Diretriz nao pode ser vazia')
        if not self.diretrizes_gerais:
            self.diretrizes_gerais = diretriz.strip()
            return
        self.diretrizes_gerais += f'\n{diretriz.strip()}'