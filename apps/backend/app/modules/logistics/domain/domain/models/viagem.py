from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4
from app.modules.logistics.domain.enums import StatusViagem

@dataclass
class Viagem:
    id: UUID
    linha_id: UUID
    veiculo_id: UUID
    motorista_id: UUID
    data_hora_saida: datetime
    data_hora_chegada_prevista: datetime
    origem: str
    destino: str
    itinerario: list[dict[str, Any]]
    status: StatusViagem = StatusViagem.PROGRAMADA
    data_hora_chegada_real: datetime | None = None
    paradas: list[dict[str, Any]] | None = None
    passageiros_embarcados: int | None = None
    passageiros_desembarcados: int | None = None
    passageiros_transbordo: int | None = None
    carga: list[dict[str, Any]] | None = None
    volume_carga: Decimal | None = None
    peso_carga: Decimal | None = None
    valor_frete: Decimal | None = None
    quilometragem_inicial: int | None = None
    quilometragem_final: int | None = None
    consumo_combustivel: Decimal | None = None
    observacoes: str | None = None

    @classmethod
    def programar(cls, *, linha_id: UUID, veiculo_id: UUID, motorista_id: UUID, data_hora_saida: datetime, data_hora_chegada_prevista: datetime, origem: str, destino: str, itinerario: list[dict[str, Any]] | None=None, observacoes: str | None=None) -> 'Viagem':
        if data_hora_chegada_prevista <= data_hora_saida:
            raise ValueError('Data/hora de chegada prevista deve ser maior que a saida')
        return cls(id=uuid4(), linha_id=linha_id, veiculo_id=veiculo_id, motorista_id=motorista_id, data_hora_saida=data_hora_saida, data_hora_chegada_prevista=data_hora_chegada_prevista, origem=origem.strip(), destino=destino.strip(), itinerario=itinerario or [], status=StatusViagem.PROGRAMADA, observacoes=observacoes)

    def iniciar(self) -> None:
        if self.status != StatusViagem.PROGRAMADA:
            raise ValueError('Viagem precisa estar programada')
        self.status = StatusViagem.EM_ANDAMENTO

    def concluir(self, data_hora_chegada: datetime) -> None:
        if self.status != StatusViagem.EM_ANDAMENTO:
            raise ValueError('Viagem precisa estar em andamento')
        if data_hora_chegada < self.data_hora_saida:
            raise ValueError('Data/hora de chegada real invalida')
        self.status = StatusViagem.CONCLUIDA
        self.data_hora_chegada_real = data_hora_chegada

    def cancelar(self, motivo: str) -> None:
        if self.status == StatusViagem.CONCLUIDA:
            raise ValueError('Viagem concluida nao pode ser cancelada')
        if not motivo.strip():
            raise ValueError('Motivo do cancelamento e obrigatorio')
        self.status = StatusViagem.CANCELADA
        self.observacoes = motivo.strip()

    def registrar_atraso(self, minutos: int) -> None:
        if minutos <= 0:
            raise ValueError('Atraso deve ser maior que zero')
        if self.status not in {StatusViagem.PROGRAMADA, StatusViagem.EM_ANDAMENTO}:
            raise ValueError('Atraso so pode ser registrado para viagem ativa')
        self.status = StatusViagem.ATRASADA
        if not self.observacoes:
            self.observacoes = f'Atraso de {minutos} minutos'
