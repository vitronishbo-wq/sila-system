from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from apps.backend.app.modules.infrastructure.domain.enums import NaturezaObra, StatusObra, TipoObra
from apps.backend.app.modules.infrastructure.domain.models.aditivo_contratual import (
    AditivoContratual,
)
from apps.backend.app.modules.infrastructure.domain.models.fiscalizacao_obra import FiscalizacaoObra
from apps.backend.app.modules.infrastructure.domain.models.medicao_obra import MedicaoObra
from apps.backend.app.modules.infrastructure.domain.models.termo_recebimento import TermoRecebimento


@dataclass
class Obra:
    id: UUID
    codigo_obra: str
    nome: str
    tipo: TipoObra
    natureza: NaturezaObra
    status: StatusObra
    orgao_responsavel_id: UUID
    orgao_responsavel_tipo: str
    valor_orcado: Decimal
    data_inicio_prevista: date
    data_fim_prevista: date
    endereco: str
    bairro: str
    municipio: str
    provincia: str
    prazo_original_dias: int
    data_cadastro: date
    descricao: str | None = None
    gestor_responsavel_id: UUID | None = None
    fiscal_responsavel_id: UUID | None = None
    empreiteira_id: UUID | None = None
    contrato_id: UUID | None = None
    projeto_id: UUID | None = None
    valor_contratado: Decimal | None = None
    valor_executado: Decimal | None = None
    valor_pago: Decimal | None = None
    data_inicio_real: date | None = None
    data_fim_real: date | None = None
    data_entrega: date | None = None
    coordenadas_lat: Decimal | None = None
    coordenadas_long: Decimal | None = None
    imovel_id: UUID | None = None
    percentual_executado: Decimal = Decimal("0")
    prazo_adicionado_dias: int = 0
    dias_corridos: int = 0
    dias_atraso: int = 0
    data_atualizacao: date | None = None
    observacoes: str | None = None
    medicoes: list[dict] = field(default_factory=list)
    aditivos: list[dict] = field(default_factory=list)
    fiscalizacoes: list[dict] = field(default_factory=list)
    termos_recebimento: list[dict] = field(default_factory=list)
    trilha_auditoria: list[dict] = field(default_factory=list)

    @classmethod
    def criar(
        cls,
        *,
        codigo_obra: str,
        nome: str,
        tipo: TipoObra,
        natureza: NaturezaObra,
        orgao_responsavel_id: UUID,
        orgao_responsavel_tipo: str,
        valor_orcado: Decimal,
        data_inicio_prevista: date,
        data_fim_prevista: date,
        endereco: str,
        bairro: str,
        municipio: str,
        provincia: str,
        descricao: str | None = None,
    ) -> Obra:
        if not codigo_obra.strip():
            raise ValueError("Codigo da obra e obrigatorio")
        if not nome.strip():
            raise ValueError("Nome da obra e obrigatorio")
        if not orgao_responsavel_tipo.strip():
            raise ValueError("Tipo do orgao responsavel e obrigatorio")
        if valor_orcado <= Decimal("0"):
            raise ValueError("Valor orcado deve ser maior que zero")
        if data_fim_prevista <= data_inicio_prevista:
            raise ValueError("Data fim prevista deve ser maior que data inicio prevista")
        if (
            not endereco.strip()
            or not bairro.strip()
            or (not municipio.strip())
            or (not provincia.strip())
        ):
            raise ValueError("Endereco, bairro, municipio e provincia sao obrigatorios")
        prazo_original = (data_fim_prevista - data_inicio_prevista).days
        return cls(
            id=uuid4(),
            codigo_obra=codigo_obra.strip(),
            nome=nome.strip(),
            descricao=descricao.strip() if descricao else None,
            tipo=tipo,
            natureza=natureza,
            status=StatusObra.PROJETO,
            orgao_responsavel_id=orgao_responsavel_id,
            orgao_responsavel_tipo=orgao_responsavel_tipo.strip(),
            valor_orcado=valor_orcado.quantize(Decimal("0.01")),
            data_inicio_prevista=data_inicio_prevista,
            data_fim_prevista=data_fim_prevista,
            endereco=endereco.strip(),
            bairro=bairro.strip(),
            municipio=municipio.strip(),
            provincia=provincia.strip(),
            prazo_original_dias=prazo_original,
            data_cadastro=date.today(),
        )

    def iniciar_licitacao(self) -> None:
        if self.status != StatusObra.PROJETO:
            raise ValueError("Obra precisa estar em fase de projeto")
        self.status = StatusObra.LICITACAO
        self.data_atualizacao = date.today()

    def contratar(self, *, contrato_id: UUID, empreiteira_id: UUID, valor: Decimal) -> None:
        if self.status != StatusObra.LICITACAO:
            raise ValueError("Obra precisa estar em licitacao")
        if valor <= Decimal("0"):
            raise ValueError("Valor contratado deve ser maior que zero")
        self.status = StatusObra.CONTRATADA
        self.contrato_id = contrato_id
        self.empreiteira_id = empreiteira_id
        self.valor_contratado = valor.quantize(Decimal("0.01"))
        self.data_atualizacao = date.today()

    def iniciar_execucao(self, data_inicio: date) -> None:
        if self.status != StatusObra.CONTRATADA:
            raise ValueError("Obra precisa estar contratada")
        self.status = StatusObra.EM_EXECUCAO
        self.data_inicio_real = data_inicio
        self.data_atualizacao = date.today()

    def atualizar_progresso(self, percentual: Decimal) -> None:
        if self.status != StatusObra.EM_EXECUCAO:
            raise ValueError("Obra nao esta em execucao")
        if percentual < Decimal("0") or percentual > Decimal("100"):
            raise ValueError("Percentual executado deve estar entre 0 e 100")
        self.percentual_executado = percentual.quantize(Decimal("0.01"))
        self.data_atualizacao = date.today()
        hoje = date.today()
        self.dias_corridos = (hoje - self.data_inicio_real).days if self.data_inicio_real else 0
        dias_previstos_corridos = max((hoje - self.data_inicio_prevista).days, 0)
        limite = self.prazo_original_dias + self.prazo_adicionado_dias
        self.dias_atraso = max(dias_previstos_corridos - limite, 0)

    def registrar_medicao(self, valor: Decimal) -> None:
        if valor <= Decimal("0"):
            raise ValueError("Valor de medicao deve ser maior que zero")
        self.valor_executado = (self.valor_executado or Decimal("0")) + valor
        self.valor_executado = self.valor_executado.quantize(Decimal("0.01"))
        self.data_atualizacao = date.today()

    def registrar_medicao_detalhada(self, medicao: MedicaoObra) -> None:
        if self.status != StatusObra.EM_EXECUCAO:
            raise ValueError("Medicao detalhada exige obra em execucao")
        self.medicoes.append(medicao.to_dict())
        self.registrar_medicao(medicao.valor_medido)
        self.percentual_executado = medicao.percentual_executado
        self.data_atualizacao = date.today()

    def registrar_pagamento(self, valor: Decimal) -> None:
        if valor <= Decimal("0"):
            raise ValueError("Valor de pagamento deve ser maior que zero")
        self.valor_pago = (self.valor_pago or Decimal("0")) + valor
        self.valor_pago = self.valor_pago.quantize(Decimal("0.01"))
        self.data_atualizacao = date.today()

    def registrar_aditivo(self, aditivo: AditivoContratual) -> None:
        if self.status not in {StatusObra.CONTRATADA, StatusObra.EM_EXECUCAO, StatusObra.SUSPENSA}:
            raise ValueError("Aditivo exige obra contratada, em execucao ou suspensa")
        self.aditivos.append(aditivo.to_dict())
        self.prazo_adicionado_dias += aditivo.prazo_adicional_dias
        if aditivo.valor_aditivo > Decimal("0"):
            self.valor_orcado = (self.valor_orcado + aditivo.valor_aditivo).quantize(
                Decimal("0.01")
            )
            if self.valor_contratado is not None:
                self.valor_contratado = (self.valor_contratado + aditivo.valor_aditivo).quantize(
                    Decimal("0.01")
                )
        self.data_atualizacao = date.today()

    def registrar_fiscalizacao(self, fiscalizacao: FiscalizacaoObra) -> None:
        if self.status not in {StatusObra.CONTRATADA, StatusObra.EM_EXECUCAO, StatusObra.SUSPENSA}:
            raise ValueError("Fiscalizacao exige obra ativa")
        self.fiscalizacoes.append(fiscalizacao.to_dict())
        if not fiscalizacao.conformidade:
            self.observacoes = fiscalizacao.apontamentos
        self.data_atualizacao = date.today()

    def suspender(self, motivo: str) -> None:
        if self.status != StatusObra.EM_EXECUCAO:
            raise ValueError("Apenas obras em execucao podem ser suspensas")
        if not motivo.strip():
            raise ValueError("Motivo da suspensao e obrigatorio")
        self.status = StatusObra.SUSPENSA
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()

    def retomar(self) -> None:
        if self.status != StatusObra.SUSPENSA:
            raise ValueError("Apenas obras suspensas podem ser retomadas")
        self.status = StatusObra.EM_EXECUCAO
        self.data_atualizacao = date.today()

    def concluir(self, data_conclusao: date) -> None:
        if self.status != StatusObra.EM_EXECUCAO:
            raise ValueError("Apenas obras em execucao podem ser concluidas")
        self.status = StatusObra.CONCLUIDA
        self.data_fim_real = data_conclusao
        self.percentual_executado = Decimal("100")
        self.data_atualizacao = date.today()

    def entregar(self, data_entrega: date) -> None:
        if self.status != StatusObra.CONCLUIDA:
            raise ValueError("Apenas obras concluidas podem ser entregues")
        self.status = StatusObra.ENTREGUE
        self.data_entrega = data_entrega
        self.data_atualizacao = date.today()

    def registrar_termo_recebimento(self, termo: TermoRecebimento) -> None:
        if self.status not in {StatusObra.CONCLUIDA, StatusObra.ENTREGUE}:
            raise ValueError("Termo de recebimento exige obra concluida ou entregue")
        self.termos_recebimento.append(termo.to_dict())
        if termo.tipo == "definitivo":
            self.status = StatusObra.ENTREGUE
            self.data_entrega = termo.data_termo
        self.data_atualizacao = date.today()

    def registrar_evento_auditoria(self, *, evento: str, payload: dict | None = None) -> None:
        self.trilha_auditoria.append(
            {"data": date.today().isoformat(), "evento": evento, "payload": payload or {}}
        )
        self.data_atualizacao = date.today()
