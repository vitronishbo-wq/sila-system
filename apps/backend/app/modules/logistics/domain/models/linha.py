from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

from apps.backend.app.modules.logistics.domain.enums import ModalTransporte, StatusLinha, TipoViagem


@dataclass
class Linha:
    id: UUID
    codigo: str
    nome: str
    modal: ModalTransporte
    tipo_viagem: TipoViagem
    origem: str
    destino: str
    itinerario: list[dict[str, Any]]
    extensao_km: Decimal
    tempo_estimado_minutos: int
    dias_operacao: list[str]
    horario_inicio: str
    horario_fim: str
    tarifa_base: Decimal
    operadora_id: UUID
    status: StatusLinha = StatusLinha.ATIVA
    data_cadastro: date = field(default_factory=date.today)
    frequencia_media_minutos: int | None = None
    concessionaria_id: UUID | None = None
    outorga_id: UUID | None = None
    data_inicio_operacao: date | None = None
    data_autorizacao: date | None = None
    data_validade_autorizacao: date | None = None
    frota_necessaria: int | None = None
    frota_operante: int | None = None
    demanda_media_diaria: int | None = None
    oferta_media_diaria: int | None = None
    ocupacao_media: Decimal | None = None
    regularidade: Decimal | None = None
    pontualidade: Decimal | None = None
    acessivel: bool = False
    ar_condicionado: bool = False
    wifi: bool = False
    sanitario: bool = False
    observacoes: str | None = None
    data_atualizacao: date | None = None
    veiculos_ativos: list[dict] = field(default_factory=list)
    trilha_auditoria: list[dict] = field(default_factory=list)

    @classmethod
    def criar(
        cls,
        *,
        codigo: str,
        nome: str,
        modal: ModalTransporte,
        tipo_viagem: TipoViagem,
        origem: str,
        destino: str,
        itinerario: list[dict[str, Any]],
        extensao_km: Decimal,
        tempo_estimado_minutos: int,
        dias_operacao: list[str],
        horario_inicio: str,
        horario_fim: str,
        tarifa_base: Decimal,
        operadora_id: UUID,
        frequencia_media_minutos: int | None = None,
        observacoes: str | None = None,
    ) -> Linha:
        if not codigo.strip():
            raise ValueError("Codigo da linha e obrigatorio")
        if not nome.strip():
            raise ValueError("Nome da linha e obrigatorio")
        if not origem.strip() or not destino.strip():
            raise ValueError("Origem e destino sao obrigatorios")
        if extensao_km <= Decimal("0"):
            raise ValueError("Extensao da linha deve ser maior que zero")
        if tempo_estimado_minutos <= 0:
            raise ValueError("Tempo estimado da linha deve ser maior que zero")
        if tarifa_base <= Decimal("0"):
            raise ValueError("Tarifa base da linha deve ser maior que zero")
        if not dias_operacao:
            raise ValueError("Dias de operacao da linha sao obrigatorios")
        if not itinerario:
            raise ValueError("Itinerario da linha e obrigatorio")
        return cls(
            id=uuid4(),
            codigo=codigo.strip(),
            nome=nome.strip(),
            modal=modal,
            tipo_viagem=tipo_viagem,
            origem=origem.strip(),
            destino=destino.strip(),
            itinerario=itinerario,
            extensao_km=extensao_km.quantize(Decimal("0.01")),
            tempo_estimado_minutos=tempo_estimado_minutos,
            dias_operacao=dias_operacao,
            horario_inicio=horario_inicio,
            horario_fim=horario_fim,
            tarifa_base=tarifa_base.quantize(Decimal("0.01")),
            operadora_id=operadora_id,
            status=StatusLinha.EM_IMPLANTACAO,
            data_cadastro=date.today(),
            frequencia_media_minutos=frequencia_media_minutos,
            observacoes=observacoes.strip() if observacoes else None,
        )

    def ativar(self) -> None:
        if self.status == StatusLinha.ATIVA:
            raise ValueError("Linha ja esta ativa")
        self.status = StatusLinha.ATIVA
        self.data_atualizacao = date.today()

    def adicionar_veiculo(self, *, veiculo_id: UUID, placa: str) -> None:
        if self.status not in {StatusLinha.ATIVA, StatusLinha.EM_IMPLANTACAO}:
            raise ValueError("Linha nao permite adicao de veiculo neste status")
        normalized = placa.strip().upper()
        if not normalized:
            raise ValueError("Placa do veiculo e obrigatoria")
        if any(item.get("placa") == normalized for item in self.veiculos_ativos):
            raise ValueError("Veiculo ja vinculado na linha")
        self.veiculos_ativos.append(
            {
                "veiculo_id": str(veiculo_id),
                "placa": normalized,
                "data_vinculo": date.today().isoformat(),
            }
        )
        self.frota_operante = len(self.veiculos_ativos)
        if self.status == StatusLinha.EM_IMPLANTACAO:
            self.status = StatusLinha.ATIVA
        self.data_atualizacao = date.today()

    def atualizar_tarifa(self, valor: Decimal) -> None:
        if valor <= Decimal("0"):
            raise ValueError("Tarifa da linha deve ser maior que zero")
        self.tarifa_base = valor.quantize(Decimal("0.01"))
        self.data_atualizacao = date.today()

    def registrar_indicadores_operacionais(
        self,
        *,
        demanda_media_diaria: int | None,
        ocupacao_media: Decimal | None,
        regularidade: Decimal | None,
        pontualidade: Decimal | None,
    ) -> None:
        self.demanda_media_diaria = demanda_media_diaria
        self.ocupacao_media = (
            ocupacao_media.quantize(Decimal("0.01")) if ocupacao_media is not None else None
        )
        self.regularidade = (
            regularidade.quantize(Decimal("0.01")) if regularidade is not None else None
        )
        self.pontualidade = (
            pontualidade.quantize(Decimal("0.01")) if pontualidade is not None else None
        )
        self.data_atualizacao = date.today()

    def registrar_evento_auditoria(self, *, evento: str, payload: dict | None = None) -> None:
        self.trilha_auditoria.append(
            {"data": date.today().isoformat(), "evento": evento, "payload": payload or {}}
        )
        self.data_atualizacao = date.today()
