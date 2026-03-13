from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusTalhao

@dataclass
class Talhao:
    id: UUID
    codigo_talhao: str
    codigo_propriedade: str
    nome: str
    area_ha: float
    tipo_solo: str | None
    irrigado: bool
    status: StatusTalhao
    data_cadastro: date

    @classmethod
    def criar(cls, *, codigo_propriedade: str, nome: str, area_ha: float, tipo_solo: str | None=None, irrigado: bool=False) -> 'Talhao':
        if area_ha <= 0:
            raise ValueError('Area do talhao deve ser maior que zero')
        return cls(id=uuid4(), codigo_talhao='', codigo_propriedade=codigo_propriedade, nome=nome, area_ha=round(area_ha, 2), tipo_solo=tipo_solo, irrigado=irrigado, status=StatusTalhao.ATIVO, data_cadastro=date.today())

    def desativar(self) -> None:
        if self.status == StatusTalhao.INATIVO:
            raise ValueError('Talhao ja esta inativo')
        self.status = StatusTalhao.INATIVO

    def ativar(self) -> None:
        if self.status == StatusTalhao.ATIVO:
            raise ValueError('Talhao ja esta ativo')
        self.status = StatusTalhao.ATIVO