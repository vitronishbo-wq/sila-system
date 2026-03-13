from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.energy.domain.enums import FonteEnergia, StatusInfraEnergia

@dataclass
class CentralGeradora:
    id: UUID
    nome: str
    tipo: FonteEnergia
    capacidade_instalada_mw: Decimal
    municipio: str
    provincia: str
    status: StatusInfraEnergia = StatusInfraEnergia.PROJETO
    data_inicio_construcao: date | None = None
    data_inicio_operacao: date | None = None
    observacoes: str | None = None

    @classmethod
    def cadastrar(cls, *, nome: str, tipo: FonteEnergia, capacidade_instalada_mw: Decimal, municipio: str, provincia: str) -> 'CentralGeradora':
        if not nome.strip():
            raise ValueError('Nome da central geradora e obrigatorio')
        if capacidade_instalada_mw <= Decimal('0'):
            raise ValueError('Capacidade instalada deve ser maior que zero')
        return cls(id=uuid4(), nome=nome.strip(), tipo=tipo, capacidade_instalada_mw=capacidade_instalada_mw, municipio=municipio.strip(), provincia=provincia.strip())

    def iniciar_construcao(self, data_inicio: date) -> None:
        if self.status != StatusInfraEnergia.PROJETO:
            raise ValueError('Central geradora precisa estar em projeto')
        self.status = StatusInfraEnergia.CONSTRUCAO
        self.data_inicio_construcao = data_inicio

    def iniciar_operacao(self, data_operacao: date) -> None:
        if self.status != StatusInfraEnergia.CONSTRUCAO:
            raise ValueError('Central geradora precisa estar em construcao')
        self.status = StatusInfraEnergia.OPERACAO
        self.data_inicio_operacao = data_operacao
