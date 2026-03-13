from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusPlantio

@dataclass
class Plantio:
    id: UUID
    codigo_plantio: str
    codigo_safra: str
    codigo_talhao: str
    area_plantada_ha: float
    quantidade_semente: float | None
    data_planejamento: date
    status: StatusPlantio
    data_execucao: date | None = None
    motivo_cancelamento: str | None = None

    @classmethod
    def planejar(cls, *, codigo_safra: str, codigo_talhao: str, area_plantada_ha: float, quantidade_semente: float | None=None) -> 'Plantio':
        if area_plantada_ha <= 0:
            raise ValueError('Area plantada deve ser maior que zero')
        if quantidade_semente is not None and quantidade_semente <= 0:
            raise ValueError('Quantidade de semente deve ser maior que zero')
        return cls(id=uuid4(), codigo_plantio='', codigo_safra=codigo_safra, codigo_talhao=codigo_talhao, area_plantada_ha=round(area_plantada_ha, 2), quantidade_semente=round(quantidade_semente, 3) if quantidade_semente is not None else None, data_planejamento=date.today(), status=StatusPlantio.PLANEJADO)

    def executar(self, data_execucao: date | None=None) -> None:
        if self.status != StatusPlantio.PLANEJADO:
            raise ValueError('Apenas plantio planejado pode ser executado')
        self.status = StatusPlantio.EXECUTADO
        self.data_execucao = data_execucao or date.today()

    def cancelar(self, motivo: str) -> None:
        if self.status == StatusPlantio.EXECUTADO:
            raise ValueError('Plantio executado nao pode ser cancelado')
        if self.status == StatusPlantio.CANCELADO:
            raise ValueError('Plantio ja esta cancelado')
        self.status = StatusPlantio.CANCELADO
        self.motivo_cancelamento = motivo