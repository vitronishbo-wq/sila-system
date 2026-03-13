from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from app.modules.infrastructure.domain.enums import StatusLicitacao, TipoLicitacao

@dataclass
class Licitacao:
    id: UUID
    numero_licitacao: str
    objeto: str
    tipo: TipoLicitacao
    status: StatusLicitacao
    obra_id: UUID
    orgao_responsavel_id: UUID
    valor_estimado: Decimal
    data_publicacao_edital: date
    data_entrega_propostas: date
    data_cadastro: date
    data_abertura: date | None = None
    vencedor_id: UUID | None = None
    valor_adjudicado: Decimal | None = None
    data_homologacao: date | None = None
    data_atualizacao: date | None = None
    observacoes: str | None = None

    @classmethod
    def abrir(cls, *, numero_licitacao: str, objeto: str, tipo: TipoLicitacao, obra_id: UUID, orgao_responsavel_id: UUID, valor_estimado: Decimal, data_publicacao_edital: date, data_entrega_propostas: date) -> 'Licitacao':
        if not numero_licitacao.strip():
            raise ValueError('Numero da licitacao e obrigatorio')
        if not objeto.strip():
            raise ValueError('Objeto da licitacao e obrigatorio')
        if valor_estimado <= Decimal('0'):
            raise ValueError('Valor estimado deve ser maior que zero')
        if data_entrega_propostas <= data_publicacao_edital:
            raise ValueError('Data de entrega deve ser maior que publicacao do edital')
        return cls(id=uuid4(), numero_licitacao=numero_licitacao.strip(), objeto=objeto.strip(), tipo=tipo, status=StatusLicitacao.EDITAL_PUBLICADO, obra_id=obra_id, orgao_responsavel_id=orgao_responsavel_id, valor_estimado=valor_estimado.quantize(Decimal('0.01')), data_publicacao_edital=data_publicacao_edital, data_entrega_propostas=data_entrega_propostas, data_cadastro=date.today())

    def iniciar_recebimento_propostas(self) -> None:
        if self.status != StatusLicitacao.EDITAL_PUBLICADO:
            raise ValueError('Licitacao precisa estar com edital publicado')
        self.status = StatusLicitacao.RECEBENDO_PROPOSTAS
        self.data_atualizacao = date.today()

    def encerrar_recebimento_propostas(self, *, data_abertura: date) -> None:
        if self.status != StatusLicitacao.RECEBENDO_PROPOSTAS:
            raise ValueError('Licitacao precisa estar recebendo propostas')
        if data_abertura < self.data_entrega_propostas:
            raise ValueError('Data de abertura nao pode ser menor que entrega de propostas')
        self.status = StatusLicitacao.PROPOSTAS_ENTREGUES
        self.data_abertura = data_abertura
        self.data_atualizacao = date.today()

    def iniciar_analise(self) -> None:
        if self.status != StatusLicitacao.PROPOSTAS_ENTREGUES:
            raise ValueError('Licitacao precisa ter propostas entregues')
        self.status = StatusLicitacao.EM_ANALISE
        self.data_atualizacao = date.today()

    def abrir_habilitacao(self) -> None:
        if self.status != StatusLicitacao.EM_ANALISE:
            raise ValueError('Licitacao precisa estar em analise')
        self.status = StatusLicitacao.HABILITACAO
        self.data_atualizacao = date.today()

    def iniciar_recursos(self) -> None:
        if self.status != StatusLicitacao.HABILITACAO:
            raise ValueError('Licitacao precisa estar em habilitacao')
        self.status = StatusLicitacao.RECURSOS
        self.data_atualizacao = date.today()

    def adjudicar(self, *, vencedor_id: UUID, valor_adjudicado: Decimal) -> None:
        if self.status not in {StatusLicitacao.HABILITACAO, StatusLicitacao.RECURSOS}:
            raise ValueError('Licitacao nao pode ser adjudicada neste status')
        if valor_adjudicado <= Decimal('0'):
            raise ValueError('Valor adjudicado deve ser maior que zero')
        self.status = StatusLicitacao.ADJUDICADA
        self.vencedor_id = vencedor_id
        self.valor_adjudicado = valor_adjudicado.quantize(Decimal('0.01'))
        self.data_atualizacao = date.today()

    def homologar(self, *, data_homologacao: date | None=None) -> None:
        if self.status != StatusLicitacao.ADJUDICADA:
            raise ValueError('Licitacao precisa estar adjudicada')
        self.status = StatusLicitacao.HOMOLOGADA
        self.data_homologacao = data_homologacao or date.today()
        self.data_atualizacao = date.today()

    def declarar_deserta(self, motivo: str) -> None:
        if self.status not in {StatusLicitacao.RECEBENDO_PROPOSTAS, StatusLicitacao.PROPOSTAS_ENTREGUES}:
            raise ValueError('Licitacao nao pode ser declarada deserta neste status')
        if not motivo.strip():
            raise ValueError('Motivo da declaracao de deserta e obrigatorio')
        self.status = StatusLicitacao.DESERTA
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()

    def revogar(self, motivo: str) -> None:
        if self.status in {StatusLicitacao.HOMOLOGADA, StatusLicitacao.REVOGADA, StatusLicitacao.ANULADA}:
            raise ValueError('Licitacao nao pode ser revogada neste status')
        if not motivo.strip():
            raise ValueError('Motivo da revogacao e obrigatorio')
        self.status = StatusLicitacao.REVOGADA
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()

    def anular(self, motivo: str) -> None:
        if self.status in {StatusLicitacao.ANULADA, StatusLicitacao.HOMOLOGADA}:
            raise ValueError('Licitacao nao pode ser anulada neste status')
        if not motivo.strip():
            raise ValueError('Motivo da anulacao e obrigatorio')
        self.status = StatusLicitacao.ANULADA
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()
