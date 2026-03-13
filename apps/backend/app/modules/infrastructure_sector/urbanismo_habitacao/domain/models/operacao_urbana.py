from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusOperacaoUrbana, TipoOperacaoUrbana

@dataclass
class OperacaoUrbana:
    id: UUID
    codigo_operacao: str
    nome: str
    tipo: TipoOperacaoUrbana
    status: StatusOperacaoUrbana
    plano_diretor_id: UUID
    orgao_responsavel_id: UUID
    provincia: str
    municipio: str | None = None
    area_intervencao: Decimal | None = None
    investimento_previsto: Decimal | None = None
    investimento_executado: Decimal | None = None
    data_inicio_prevista: date | None = None
    data_fim_prevista: date | None = None
    data_inicio_real: date | None = None
    data_fim_real: date | None = None
    percentual_execucao: Decimal = Decimal('0')
    data_cadastro: date = field(default_factory=date.today)
    data_atualizacao: date | None = None
    observacoes: str | None = None

    @classmethod
    def criar(cls, *, codigo_operacao: str, nome: str, tipo: TipoOperacaoUrbana, plano_diretor_id: UUID, orgao_responsavel_id: UUID, provincia: str, municipio: str | None=None, area_intervencao: Decimal | None=None, investimento_previsto: Decimal | None=None, data_inicio_prevista: date | None=None, data_fim_prevista: date | None=None) -> 'OperacaoUrbana':
        if not codigo_operacao.strip():
            raise ValueError('Codigo da operacao e obrigatorio')
        if not nome.strip():
            raise ValueError('Nome da operacao e obrigatorio')
        if not provincia.strip():
            raise ValueError('Provincia e obrigatoria')
        if data_inicio_prevista and data_fim_prevista and (data_fim_prevista <= data_inicio_prevista):
            raise ValueError('Data fim prevista deve ser maior que data inicio prevista')
        return cls(id=uuid4(), codigo_operacao=codigo_operacao.strip(), nome=nome.strip(), tipo=tipo, status=StatusOperacaoUrbana.ELABORACAO, plano_diretor_id=plano_diretor_id, orgao_responsavel_id=orgao_responsavel_id, provincia=provincia.strip(), municipio=municipio.strip() if municipio else None, area_intervencao=area_intervencao, investimento_previsto=investimento_previsto, data_inicio_prevista=data_inicio_prevista, data_fim_prevista=data_fim_prevista)

    def aprovar(self) -> None:
        if self.status != StatusOperacaoUrbana.ELABORACAO:
            raise ValueError('Operacao precisa estar em elaboracao')
        self.status = StatusOperacaoUrbana.APROVADA
        self.data_atualizacao = date.today()

    def iniciar_execucao(self, *, data_inicio_real: date) -> None:
        if self.status != StatusOperacaoUrbana.APROVADA:
            raise ValueError('Operacao precisa estar aprovada')
        self.status = StatusOperacaoUrbana.EM_EXECUCAO
        self.data_inicio_real = data_inicio_real
        self.data_atualizacao = date.today()

    def atualizar_execucao(self, *, percentual_execucao: Decimal, investimento_executado: Decimal | None=None) -> None:
        if self.status != StatusOperacaoUrbana.EM_EXECUCAO:
            raise ValueError('Operacao precisa estar em execucao')
        if percentual_execucao < 0 or percentual_execucao > 100:
            raise ValueError('Percentual de execucao deve estar entre 0 e 100')
        self.percentual_execucao = percentual_execucao
        if investimento_executado is not None:
            self.investimento_executado = investimento_executado
        self.data_atualizacao = date.today()

    def concluir(self, *, data_fim_real: date) -> None:
        if self.status != StatusOperacaoUrbana.EM_EXECUCAO:
            raise ValueError('Operacao precisa estar em execucao')
        if self.data_inicio_real and data_fim_real <= self.data_inicio_real:
            raise ValueError('Data fim real deve ser maior que data inicio real')
        self.status = StatusOperacaoUrbana.CONCLUIDA
        self.data_fim_real = data_fim_real
        self.percentual_execucao = Decimal('100')
        self.data_atualizacao = date.today()

    def suspender(self, *, motivo: str) -> None:
        if self.status != StatusOperacaoUrbana.EM_EXECUCAO:
            raise ValueError('Apenas operacao em execucao pode ser suspensa')
        if not motivo.strip():
            raise ValueError('Motivo da suspensao e obrigatorio')
        self.status = StatusOperacaoUrbana.SUSPENSA
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()

    def retomar(self) -> None:
        if self.status != StatusOperacaoUrbana.SUSPENSA:
            raise ValueError('Apenas operacao suspensa pode ser retomada')
        self.status = StatusOperacaoUrbana.EM_EXECUCAO
        self.data_atualizacao = date.today()

    def cancelar(self, *, motivo: str) -> None:
        if self.status in {StatusOperacaoUrbana.CONCLUIDA, StatusOperacaoUrbana.CANCELADA}:
            raise ValueError('Operacao nao pode ser cancelada neste status')
        if not motivo.strip():
            raise ValueError('Motivo do cancelamento e obrigatorio')
        self.status = StatusOperacaoUrbana.CANCELADA
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()