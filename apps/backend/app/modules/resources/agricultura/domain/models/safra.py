from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from app.modules.resources.agricultura.domain.enums import StatusSafra

@dataclass
class Safra:
    id: UUID
    codigo_safra: str
    propriedade_id: UUID
    cultura_id: UUID
    ano: int
    area_plantada_ha: float
    producao_estimada_ton: float
    status: StatusSafra
    data_inicio: date | None = None
    data_colheita: date | None = None
    producao_real_ton: float | None = None

    @classmethod
    def criar(cls, *, propriedade_id: UUID, cultura_id: UUID, ano: int, area_plantada_ha: float, producao_estimada_ton: float) -> 'Safra':
        if ano < 2000:
            raise ValueError('Ano da safra invalido')
        if area_plantada_ha <= 0:
            raise ValueError('Area plantada deve ser maior que zero')
        if producao_estimada_ton < 0:
            raise ValueError('Producao estimada nao pode ser negativa')
        return cls(id=uuid4(), codigo_safra='', propriedade_id=propriedade_id, cultura_id=cultura_id, ano=ano, area_plantada_ha=round(area_plantada_ha, 2), producao_estimada_ton=round(producao_estimada_ton, 2), status=StatusSafra.PLANEJADA)

    def iniciar(self) -> None:
        if self.status != StatusSafra.PLANEJADA:
            raise ValueError('Apenas safras planejadas podem ser iniciadas')
        self.status = StatusSafra.EM_ANDAMENTO
        self.data_inicio = date.today()

    def colher(self, producao_real_ton: float) -> None:
        if self.status != StatusSafra.EM_ANDAMENTO:
            raise ValueError('Apenas safras em andamento podem ser colhidas')
        if producao_real_ton < 0:
            raise ValueError('Producao real nao pode ser negativa')
        self.status = StatusSafra.COLHIDA
        self.data_colheita = date.today()
        self.producao_real_ton = round(producao_real_ton, 2)