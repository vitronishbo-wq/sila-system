from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import StatusOutorga, TipoCaptacao, TipoOutorga, TipoUso

@dataclass
class Outorga:
    id: UUID
    numero_outorga: str
    tipo: TipoOutorga
    status: StatusOutorga
    requerente_id: UUID
    requerente_tipo: str
    corpo_hidrico_id: UUID
    vazao: Decimal
    unidade_vazao: str
    finalidade_uso: TipoUso
    data_requerimento: date
    tipo_captacao: TipoCaptacao | None = None
    tempo_captacao: int | None = None
    periodo_captacao: str | None = None
    data_validade_inicio: date | None = None
    data_validade_fim: date | None = None
    data_publicacao: date | None = None
    processo_administrativo: str | None = None
    coordenadas_lat: Decimal | None = None
    coordenadas_long: Decimal | None = None
    observacoes: str | None = None

    @classmethod
    def requerer(cls, *, tipo: TipoOutorga, requerente_id: UUID, requerente_tipo: str, corpo_hidrico_id: UUID, vazao: Decimal, unidade_vazao: str, finalidade_uso: TipoUso, numero_outorga: str='', tipo_captacao: TipoCaptacao | None=None, tempo_captacao: int | None=None, periodo_captacao: str | None=None, coordenadas_lat: Decimal | None=None, coordenadas_long: Decimal | None=None) -> 'Outorga':
        if vazao <= Decimal('0'):
            raise ValueError('Vazao deve ser maior que zero')
        if not unidade_vazao.strip():
            raise ValueError('Unidade de vazao e obrigatoria')
        if not requerente_tipo.strip():
            raise ValueError('Tipo do requerente e obrigatorio')
        if tempo_captacao is not None and tempo_captacao <= 0:
            raise ValueError('Tempo de captacao deve ser maior que zero')
        return cls(id=uuid4(), numero_outorga=numero_outorga, tipo=tipo, status=StatusOutorga.REQUERIDA, requerente_id=requerente_id, requerente_tipo=requerente_tipo.strip(), corpo_hidrico_id=corpo_hidrico_id, tipo_captacao=tipo_captacao, vazao=vazao.quantize(Decimal('0.01')), unidade_vazao=unidade_vazao.strip(), tempo_captacao=tempo_captacao, periodo_captacao=periodo_captacao.strip() if periodo_captacao else None, finalidade_uso=finalidade_uso, data_requerimento=date.today(), coordenadas_lat=coordenadas_lat, coordenadas_long=coordenadas_long)

    def iniciar_analise(self) -> None:
        if self.status != StatusOutorga.REQUERIDA:
            raise ValueError('Apenas outorga requerida pode entrar em analise')
        self.status = StatusOutorga.EM_ANALISE

    def deferir(self, *, data_validade_inicio: date, data_validade_fim: date, data_publicacao: date, processo: str) -> None:
        if self.status != StatusOutorga.EM_ANALISE:
            raise ValueError('Outorga precisa estar em analise')
        if data_validade_fim <= data_validade_inicio:
            raise ValueError('Data final deve ser maior que data inicial')
        if not processo.strip():
            raise ValueError('Processo administrativo e obrigatorio')
        self.status = StatusOutorga.DEFERIDA
        self.data_validade_inicio = data_validade_inicio
        self.data_validade_fim = data_validade_fim
        self.data_publicacao = data_publicacao
        self.processo_administrativo = processo.strip()
        self.observacoes = None

    def indeferir(self, motivo: str) -> None:
        if self.status not in {StatusOutorga.REQUERIDA, StatusOutorga.EM_ANALISE}:
            raise ValueError('Outorga nao pode ser indeferida neste status')
        if not motivo.strip():
            raise ValueError('Motivo do indeferimento e obrigatorio')
        self.status = StatusOutorga.INDEFERIDA
        self.observacoes = motivo.strip()

    def cancelar(self, motivo: str) -> None:
        if self.status in {StatusOutorga.CANCELADA, StatusOutorga.INDEFERIDA}:
            raise ValueError('Outorga ja encerrada')
        if not motivo.strip():
            raise ValueError('Motivo do cancelamento e obrigatorio')
        self.status = StatusOutorga.CANCELADA
        self.observacoes = motivo.strip()

    def suspender(self, motivo: str) -> None:
        if self.status != StatusOutorga.DEFERIDA:
            raise ValueError('Apenas outorga deferida pode ser suspensa')
        if not motivo.strip():
            raise ValueError('Motivo da suspensao e obrigatorio')
        self.status = StatusOutorga.SUSPENSA
        self.observacoes = motivo.strip()

    def renovar(self, nova_data_fim: date) -> None:
        if self.status not in {StatusOutorga.DEFERIDA, StatusOutorga.SUSPENSA}:
            raise ValueError('Apenas outorgas deferidas/suspensas podem ser renovadas')
        data_base = self.data_validade_fim or self.data_validade_inicio
        if data_base is None:
            raise ValueError('Outorga sem vigencia para renovacao')
        if nova_data_fim <= data_base:
            raise ValueError('Nova data fim deve ser posterior a vigencia atual')
        self.data_validade_fim = nova_data_fim
        if self.status == StatusOutorga.SUSPENSA:
            self.status = StatusOutorga.DEFERIDA
        self.observacoes = None

    def atualizar_status_vencimento(self) -> None:
        if self.status == StatusOutorga.DEFERIDA and self.data_validade_fim and (date.today() > self.data_validade_fim):
            self.status = StatusOutorga.VENCIDA