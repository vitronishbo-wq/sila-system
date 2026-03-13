from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4
from apps.backend.app.modules.tourism.domain.enums import StatusReserva, TipoTarifa

@dataclass
class ReservaHotel:
    id: UUID
    codigo_reserva: str
    hotel_id: UUID
    cliente_nome: str
    cliente_documento: str
    cliente_nacionalidade: str
    quartos: int
    adultos: int
    criancas: int
    checkin: date
    checkout: date
    noites: int
    valor_diaria: Decimal
    valor_total: Decimal
    tipo_tarifa: TipoTarifa
    status: StatusReserva
    data_reserva: datetime
    cliente_id: Optional[UUID] = None
    data_checkin_real: Optional[datetime] = None
    data_checkout_real: Optional[datetime] = None
    observacoes: Optional[str] = None

    @classmethod
    def criar(cls, *, hotel_id: UUID, cliente_nome: str, cliente_documento: str, cliente_nacionalidade: str, quartos: int, adultos: int, criancas: int, checkin: date, checkout: date, valor_diaria: Decimal) -> 'ReservaHotel':
        if checkout <= checkin:
            raise ValueError('Checkout deve ser posterior ao checkin')
        if quartos <= 0:
            raise ValueError('Quantidade de quartos deve ser maior que zero')
        if adultos <= 0:
            raise ValueError('Reserva deve ter pelo menos um adulto')
        if valor_diaria <= 0:
            raise ValueError('Valor da diaria deve ser maior que zero')
        noites = (checkout - checkin).days
        valor_total = valor_diaria * noites * quartos
        return cls(id=uuid4(), codigo_reserva='', hotel_id=hotel_id, cliente_nome=cliente_nome.strip(), cliente_documento=cliente_documento.strip(), cliente_nacionalidade=cliente_nacionalidade.strip(), quartos=quartos, adultos=adultos, criancas=criancas, checkin=checkin, checkout=checkout, noites=noites, valor_diaria=valor_diaria, valor_total=valor_total, tipo_tarifa=TipoTarifa.NORMAL, status=StatusReserva.PENDENTE, data_reserva=datetime.now())

    def confirmar(self) -> None:
        if self.status != StatusReserva.PENDENTE:
            raise ValueError('Reserva precisa estar pendente')
        self.status = StatusReserva.CONFIRMADA

    def cancelar(self, motivo: str) -> None:
        if self.status == StatusReserva.REALIZADA:
            raise ValueError('Reserva realizada nao pode ser cancelada')
        self.status = StatusReserva.CANCELADA
        self.observacoes = motivo.strip()

    def realizar_checkin(self) -> None:
        if self.status != StatusReserva.CONFIRMADA:
            raise ValueError('Reserva precisa estar confirmada')
        self.status = StatusReserva.REALIZADA
        self.data_checkin_real = datetime.now()

    def realizar_checkout(self) -> None:
        if self.status != StatusReserva.REALIZADA:
            raise ValueError('Hospede ainda nao realizou checkin')
        self.data_checkout_real = datetime.now()
