from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.energy.domain.enums import ClasseTensao, StatusInfraEnergia

@dataclass
class Subestacao:
    id: UUID
    nome: str
    tensao_nominal_kv: Decimal
    classe_tensao: ClasseTensao
    municipio: str
    provincia: str
    status: StatusInfraEnergia = StatusInfraEnergia.PROJETO
    data_inicio_construcao: date | None = None
    data_inicio_operacao: date | None = None
    observacoes: str | None = None

    @classmethod
    def cadastrar(cls, *, nome: str, tensao_nominal_kv: Decimal, classe_tensao: ClasseTensao, municipio: str, provincia: str) -> 'Subestacao':
        if not nome.strip():
            raise ValueError('Nome da subestacao e obrigatorio')
        if tensao_nominal_kv <= Decimal('0'):
            raise ValueError('Tensao nominal deve ser maior que zero')
        return cls(id=uuid4(), nome=nome.strip(), tensao_nominal_kv=tensao_nominal_kv, classe_tensao=classe_tensao, municipio=municipio.strip(), provincia=provincia.strip())

    def iniciar_construcao(self, data_inicio: date) -> None:
        if self.status != StatusInfraEnergia.PROJETO:
            raise ValueError('Subestacao precisa estar em projeto')
        self.status = StatusInfraEnergia.CONSTRUCAO
        self.data_inicio_construcao = data_inicio

    def iniciar_operacao(self, data_operacao: date) -> None:
        if self.status != StatusInfraEnergia.CONSTRUCAO:
            raise ValueError('Subestacao precisa estar em construcao')
        self.status = StatusInfraEnergia.OPERACAO
        self.data_inicio_operacao = data_operacao
