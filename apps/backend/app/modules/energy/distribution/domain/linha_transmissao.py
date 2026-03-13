from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from app.modules.energy.domain.enums import StatusInfraEnergia

@dataclass
class LinhaTransmissao:
    id: UUID
    origem_id: UUID
    origem_tipo: str
    destino_id: UUID
    destino_tipo: str
    capacidade_mw: Decimal
    extensao_km: Decimal
    status: StatusInfraEnergia = StatusInfraEnergia.PROJETO
    data_inicio_construcao: date | None = None
    data_inicio_operacao: date | None = None
    observacoes: str | None = None

    @classmethod
    def cadastrar(cls, *, origem_id: UUID, origem_tipo: str, destino_id: UUID, destino_tipo: str, capacidade_mw: Decimal, extensao_km: Decimal) -> 'LinhaTransmissao':
        tipos_validos = {'central_geradora', 'subestacao'}
        if origem_tipo not in tipos_validos:
            raise ValueError("origem_tipo deve ser 'central_geradora' ou 'subestacao'")
        if destino_tipo not in tipos_validos:
            raise ValueError("destino_tipo deve ser 'central_geradora' ou 'subestacao'")
        if origem_id == destino_id and origem_tipo == destino_tipo:
            raise ValueError('Origem e destino da linha de transmissao nao podem ser iguais')
        if capacidade_mw <= Decimal('0'):
            raise ValueError('Capacidade deve ser maior que zero')
        if extensao_km <= Decimal('0'):
            raise ValueError('Extensao deve ser maior que zero')
        return cls(id=uuid4(), origem_id=origem_id, origem_tipo=origem_tipo, destino_id=destino_id, destino_tipo=destino_tipo, capacidade_mw=capacidade_mw, extensao_km=extensao_km)

    def iniciar_construcao(self, data_inicio: date) -> None:
        if self.status != StatusInfraEnergia.PROJETO:
            raise ValueError('Linha de transmissao precisa estar em projeto')
        self.status = StatusInfraEnergia.CONSTRUCAO
        self.data_inicio_construcao = data_inicio

    def iniciar_operacao(self, data_operacao: date) -> None:
        if self.status != StatusInfraEnergia.CONSTRUCAO:
            raise ValueError('Linha de transmissao precisa estar em construcao')
        self.status = StatusInfraEnergia.OPERACAO
        self.data_inicio_operacao = data_operacao
