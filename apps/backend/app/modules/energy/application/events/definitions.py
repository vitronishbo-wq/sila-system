from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from apps.backend.app.modules.energy.domain.models import ConsumoEnergia, FaturaEnergia


@dataclass(frozen=True)
class DomainEvent:
    event_id: UUID
    timestamp: datetime
    version: int = field(default=1, init=False)

    @staticmethod
    def _now() -> datetime:
        return datetime.now(UTC)


@dataclass(frozen=True)
class LeituraRealizadaEvent(DomainEvent):
    consumo_id: UUID
    unidade_consumidora_id: UUID
    medidor_id: UUID | None
    leitura_kwh: Decimal
    consumo_periodo_kwh: Decimal
    data_leitura: datetime
    tipo_leitura: str
    classe_tarifaria: str
    cpf_titular: str
    event_name = "LeituraRealizadaEvent"

    @classmethod
    def from_consumo(cls, consumo: ConsumoEnergia) -> LeituraRealizadaEvent:
        return cls(
            event_id=uuid4(),
            timestamp=DomainEvent._now(),
            consumo_id=consumo.id,
            unidade_consumidora_id=consumo.unidade_consumidora_id,
            medidor_id=consumo.medidor_id,
            leitura_kwh=consumo.leitura_kwh,
            consumo_periodo_kwh=consumo.consumo_periodo_kwh,
            data_leitura=consumo.data_leitura,
            tipo_leitura=consumo.tipo_leitura.value,
            classe_tarifaria=consumo.classe_tarifaria,
            cpf_titular=consumo.cpf_titular,
        )

    def to_payload(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "timestamp": self.timestamp.isoformat(),
            "version": self.version,
            "consumo_id": str(self.consumo_id),
            "unidade_consumidora_id": str(self.unidade_consumidora_id),
            "medidor_id": str(self.medidor_id) if self.medidor_id else None,
            "leitura_kwh": str(self.leitura_kwh),
            "consumo_periodo_kwh": str(self.consumo_periodo_kwh),
            "data_leitura": self.data_leitura.isoformat(),
            "tipo_leitura": self.tipo_leitura,
            "classe_tarifaria": self.classe_tarifaria,
            "cpf_titular": self.cpf_titular,
        }

    @classmethod
    def from_payload(cls, payload: dict) -> LeituraRealizadaEvent:
        return cls(
            event_id=UUID(payload["event_id"]),
            timestamp=datetime.fromisoformat(payload["timestamp"]),
            consumo_id=UUID(payload["consumo_id"]),
            unidade_consumidora_id=UUID(payload["unidade_consumidora_id"]),
            medidor_id=UUID(payload["medidor_id"]) if payload.get("medidor_id") else None,
            leitura_kwh=Decimal(payload["leitura_kwh"]),
            consumo_periodo_kwh=Decimal(payload["consumo_periodo_kwh"]),
            data_leitura=datetime.fromisoformat(payload["data_leitura"]),
            tipo_leitura=payload["tipo_leitura"],
            classe_tarifaria=payload["classe_tarifaria"],
            cpf_titular=payload["cpf_titular"],
        )


@dataclass(frozen=True)
class FaturaGeradaEvent(DomainEvent):
    fatura_id: UUID
    numero_fatura: str
    consumo_id: UUID
    unidade_consumidora_id: UUID
    cpf_titular: str
    consumo_kwh: Decimal
    valor_total: Decimal
    mes_referencia: str
    data_vencimento: datetime
    bandeira_tarifaria: str
    event_name = "FaturaGeradaEvent"

    @classmethod
    def from_fatura(cls, fatura: FaturaEnergia) -> FaturaGeradaEvent:
        return cls(
            event_id=uuid4(),
            timestamp=DomainEvent._now(),
            fatura_id=fatura.id,
            numero_fatura=fatura.numero_fatura,
            consumo_id=fatura.consumo_id,
            unidade_consumidora_id=fatura.unidade_consumidora_id,
            cpf_titular=fatura.cpf_titular,
            consumo_kwh=fatura.consumo_kwh,
            valor_total=fatura.valor_total,
            mes_referencia=fatura.mes_referencia,
            data_vencimento=datetime.combine(fatura.data_vencimento, datetime.min.time(), UTC),
            bandeira_tarifaria=fatura.bandeira_tarifaria.value,
        )

    def to_payload(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "timestamp": self.timestamp.isoformat(),
            "version": self.version,
            "fatura_id": str(self.fatura_id),
            "numero_fatura": self.numero_fatura,
            "consumo_id": str(self.consumo_id),
            "unidade_consumidora_id": str(self.unidade_consumidora_id),
            "cpf_titular": self.cpf_titular,
            "consumo_kwh": str(self.consumo_kwh),
            "valor_total": str(self.valor_total),
            "mes_referencia": self.mes_referencia,
            "data_vencimento": self.data_vencimento.isoformat(),
            "bandeira_tarifaria": self.bandeira_tarifaria,
        }

    @classmethod
    def from_payload(cls, payload: dict) -> FaturaGeradaEvent:
        return cls(
            event_id=UUID(payload["event_id"]),
            timestamp=datetime.fromisoformat(payload["timestamp"]),
            fatura_id=UUID(payload["fatura_id"]),
            numero_fatura=payload["numero_fatura"],
            consumo_id=UUID(payload["consumo_id"]),
            unidade_consumidora_id=UUID(payload["unidade_consumidora_id"]),
            cpf_titular=payload["cpf_titular"],
            consumo_kwh=Decimal(payload["consumo_kwh"]),
            valor_total=Decimal(payload["valor_total"]),
            mes_referencia=payload["mes_referencia"],
            data_vencimento=datetime.fromisoformat(payload["data_vencimento"]),
            bandeira_tarifaria=payload["bandeira_tarifaria"],
        )


@dataclass(frozen=True)
class InterrupcaoEvent(DomainEvent):
    trecho_rede_id: UUID
    subestacao_id: UUID | None
    data_inicio: datetime
    data_fim: datetime | None
    causa: str
    consumidores_afetados: int
    duracao_minutos: int | None = None
    event_name = "InterrupcaoEvent"

    def to_payload(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "timestamp": self.timestamp.isoformat(),
            "version": self.version,
            "trecho_rede_id": str(self.trecho_rede_id),
            "subestacao_id": str(self.subestacao_id) if self.subestacao_id else None,
            "data_inicio": self.data_inicio.isoformat(),
            "data_fim": self.data_fim.isoformat() if self.data_fim else None,
            "causa": self.causa,
            "consumidores_afetados": self.consumidores_afetados,
            "duracao_minutos": self.duracao_minutos,
        }

    @classmethod
    def from_payload(cls, payload: dict) -> InterrupcaoEvent:
        return cls(
            event_id=UUID(payload["event_id"]),
            timestamp=datetime.fromisoformat(payload["timestamp"]),
            trecho_rede_id=UUID(payload["trecho_rede_id"]),
            subestacao_id=UUID(payload["subestacao_id"]) if payload.get("subestacao_id") else None,
            data_inicio=datetime.fromisoformat(payload["data_inicio"]),
            data_fim=datetime.fromisoformat(payload["data_fim"])
            if payload.get("data_fim")
            else None,
            causa=payload["causa"],
            consumidores_afetados=int(payload["consumidores_afetados"]),
            duracao_minutos=payload.get("duracao_minutos"),
        )


@dataclass(frozen=True)
class QualidadeInconformeEvent(DomainEvent):
    ponto_medicao_id: UUID
    parametro: str
    valor_medido: Decimal
    valor_referencia: Decimal
    desvio_percentual: Decimal
    event_name = "QualidadeInconformeEvent"

    def to_payload(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "timestamp": self.timestamp.isoformat(),
            "version": self.version,
            "ponto_medicao_id": str(self.ponto_medicao_id),
            "parametro": self.parametro,
            "valor_medido": str(self.valor_medido),
            "valor_referencia": str(self.valor_referencia),
            "desvio_percentual": str(self.desvio_percentual),
        }

    @classmethod
    def from_payload(cls, payload: dict) -> QualidadeInconformeEvent:
        return cls(
            event_id=UUID(payload["event_id"]),
            timestamp=datetime.fromisoformat(payload["timestamp"]),
            ponto_medicao_id=UUID(payload["ponto_medicao_id"]),
            parametro=payload["parametro"],
            valor_medido=Decimal(payload["valor_medido"]),
            valor_referencia=Decimal(payload["valor_referencia"]),
            desvio_percentual=Decimal(payload["desvio_percentual"]),
        )


@dataclass(frozen=True)
class DemandaCriticaEvent(DomainEvent):
    subestacao_id: UUID
    demanda_atual_mw: Decimal
    capacidade_maxima_mw: Decimal
    percentual_utilizacao: Decimal
    alerta_nivel: str
    event_name = "DemandaCriticaEvent"

    def to_payload(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "timestamp": self.timestamp.isoformat(),
            "version": self.version,
            "subestacao_id": str(self.subestacao_id),
            "demanda_atual_mw": str(self.demanda_atual_mw),
            "capacidade_maxima_mw": str(self.capacidade_maxima_mw),
            "percentual_utilizacao": str(self.percentual_utilizacao),
            "alerta_nivel": self.alerta_nivel,
        }

    @classmethod
    def from_payload(cls, payload: dict) -> DemandaCriticaEvent:
        return cls(
            event_id=UUID(payload["event_id"]),
            timestamp=datetime.fromisoformat(payload["timestamp"]),
            subestacao_id=UUID(payload["subestacao_id"]),
            demanda_atual_mw=Decimal(payload["demanda_atual_mw"]),
            capacidade_maxima_mw=Decimal(payload["capacidade_maxima_mw"]),
            percentual_utilizacao=Decimal(payload["percentual_utilizacao"]),
            alerta_nivel=payload["alerta_nivel"],
        )
