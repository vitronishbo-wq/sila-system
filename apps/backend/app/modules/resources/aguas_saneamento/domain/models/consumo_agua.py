from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import (
    CategoriaConsumo,
    StatusConsumo,
)


@dataclass
class ConsumoAgua:
    id: UUID
    codigo_consumo: str
    abastecimento_id: UUID
    titular_id: UUID
    referencia: str
    categoria: CategoriaConsumo
    volume_m3: Decimal
    unidade_volume: str
    data_leitura: date
    status: StatusConsumo
    data_registro: date
    hidrometro_id: UUID | None = None
    leitura_anterior: Decimal | None = None
    leitura_atual: Decimal | None = None
    observacoes: str | None = None

    @classmethod
    def registrar(
        cls,
        *,
        abastecimento_id: UUID,
        titular_id: UUID,
        referencia: str,
        categoria: CategoriaConsumo,
        volume_m3: Decimal,
        unidade_volume: str,
        hidrometro_id: UUID | None = None,
        leitura_anterior: Decimal | None = None,
        leitura_atual: Decimal | None = None,
        data_leitura: date | None = None,
    ) -> ConsumoAgua:
        if len(referencia) != 7 or referencia[4] != "-":
            raise ValueError("Referencia deve seguir formato YYYY-MM")
        if volume_m3 <= Decimal("0"):
            raise ValueError("Volume consumido deve ser maior que zero")
        if not unidade_volume.strip():
            raise ValueError("Unidade de volume e obrigatoria")
        if (
            leitura_anterior is not None
            and leitura_atual is not None
            and (leitura_atual < leitura_anterior)
        ):
            raise ValueError("Leitura atual nao pode ser menor que leitura anterior")
        return cls(
            id=uuid4(),
            codigo_consumo="",
            abastecimento_id=abastecimento_id,
            titular_id=titular_id,
            referencia=referencia,
            categoria=categoria,
            volume_m3=volume_m3.quantize(Decimal("0.01")),
            unidade_volume=unidade_volume.strip(),
            data_leitura=data_leitura or date.today(),
            status=StatusConsumo.REGISTRADO,
            data_registro=date.today(),
            hidrometro_id=hidrometro_id,
            leitura_anterior=leitura_anterior.quantize(Decimal("0.01"))
            if leitura_anterior is not None
            else None,
            leitura_atual=leitura_atual.quantize(Decimal("0.01"))
            if leitura_atual is not None
            else None,
        )

    def validar(self) -> None:
        if self.status != StatusConsumo.REGISTRADO:
            raise ValueError("Apenas consumo registrado pode ser validado")
        self.status = StatusConsumo.VALIDADO

    def faturar(self) -> None:
        if self.status != StatusConsumo.VALIDADO:
            raise ValueError("Apenas consumo validado pode ser faturado")
        self.status = StatusConsumo.FATURADO

    def cancelar(self, motivo: str) -> None:
        if self.status == StatusConsumo.CANCELADO:
            raise ValueError("Consumo ja cancelado")
        if not motivo.strip():
            raise ValueError("Motivo do cancelamento e obrigatorio")
        self.status = StatusConsumo.CANCELADO
        self.observacoes = motivo.strip()
