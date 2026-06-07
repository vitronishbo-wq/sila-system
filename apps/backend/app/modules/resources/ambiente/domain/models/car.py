from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from apps.backend.app.modules.resources.ambiente.domain.enums import Bioma, StatusCAR, TipoImovel


@dataclass
class CAR:
    id: UUID
    numero_car: str
    imovel_id: UUID
    proprietario_id: UUID
    area_total: Decimal
    area_preservacao_permanente: Decimal
    area_reserva_legal: Decimal
    area_uso_alternativo: Decimal
    area_consolidada: Decimal
    bioma: Bioma
    tipo_imovel: TipoImovel
    status: StatusCAR
    data_cadastro: date
    data_analise: date | None = None
    data_aprovacao: date | None = None
    analista_id: UUID | None = None
    observacoes: str | None = None

    @classmethod
    def criar(
        cls,
        *,
        imovel_id: UUID,
        proprietario_id: UUID,
        area_total: Decimal,
        bioma: Bioma,
        tipo_imovel: TipoImovel,
    ) -> CAR:
        if area_total <= Decimal("0"):
            raise ValueError("Area total deve ser maior que zero")
        return cls(
            id=uuid4(),
            numero_car="",
            imovel_id=imovel_id,
            proprietario_id=proprietario_id,
            area_total=area_total.quantize(Decimal("0.01")),
            area_preservacao_permanente=Decimal("0"),
            area_reserva_legal=Decimal("0"),
            area_uso_alternativo=Decimal("0"),
            area_consolidada=Decimal("0"),
            bioma=bioma,
            tipo_imovel=tipo_imovel,
            status=StatusCAR.PENDENTE,
            data_cadastro=date.today(),
        )

    def definir_areas(
        self,
        *,
        area_preservacao_permanente: Decimal,
        area_reserva_legal: Decimal,
        area_uso_alternativo: Decimal,
        area_consolidada: Decimal,
    ) -> None:
        valores = [
            area_preservacao_permanente,
            area_reserva_legal,
            area_uso_alternativo,
            area_consolidada,
        ]
        if any(v < Decimal("0") for v in valores):
            raise ValueError("Areas nao podem ser negativas")
        soma = sum(valores, Decimal("0")).quantize(Decimal("0.01"))
        if soma > self.area_total:
            raise ValueError("Soma das areas nao pode exceder area total")
        self.area_preservacao_permanente = area_preservacao_permanente.quantize(Decimal("0.01"))
        self.area_reserva_legal = area_reserva_legal.quantize(Decimal("0.01"))
        self.area_uso_alternativo = area_uso_alternativo.quantize(Decimal("0.01"))
        self.area_consolidada = area_consolidada.quantize(Decimal("0.01"))

    def submeter_para_analise(self) -> None:
        if self.status not in {StatusCAR.PENDENTE, StatusCAR.PENDENCIA}:
            raise ValueError("Apenas CAR pendente ou com pendencia pode ser submetido")
        self.status = StatusCAR.EM_ANALISE
        self.data_analise = date.today()

    def aprovar(self, analista_id: UUID) -> None:
        if self.status != StatusCAR.EM_ANALISE:
            raise ValueError("CAR precisa estar em analise")
        self.status = StatusCAR.CADASTRADO
        self.data_aprovacao = date.today()
        self.analista_id = analista_id
        self.observacoes = None

    def solicitar_pendencia(self, motivo: str, analista_id: UUID) -> None:
        if self.status != StatusCAR.EM_ANALISE:
            raise ValueError("CAR precisa estar em analise")
        if not motivo.strip():
            raise ValueError("Motivo da pendencia e obrigatorio")
        self.status = StatusCAR.PENDENCIA
        self.observacoes = motivo.strip()
        self.analista_id = analista_id
