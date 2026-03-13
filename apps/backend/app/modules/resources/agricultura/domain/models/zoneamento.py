from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from apps.backend.app.modules.resources.agricultura.domain.enums import AptidaoSolo, StatusZoneamento, TipoZonaAgricola

@dataclass
class Zoneamento:
    id: UUID
    codigo_zoneamento: str
    codigo_propriedade: str
    zona: TipoZonaAgricola
    aptidao_solo: AptidaoSolo
    area_zoneada_ha: float
    status: StatusZoneamento
    data_zoneamento: date
    culturas_recomendadas: list[str] | None = None
    restricoes: list[str] | None = None
    validade_ate: date | None = None
    observacoes: str | None = None

    @classmethod
    def registrar(cls, *, codigo_propriedade: str, zona: TipoZonaAgricola, aptidao_solo: AptidaoSolo, area_zoneada_ha: float, culturas_recomendadas: list[str] | None=None, restricoes: list[str] | None=None, validade_ate: date | None=None, observacoes: str | None=None) -> 'Zoneamento':
        if area_zoneada_ha <= 0:
            raise ValueError('Area zoneada deve ser maior que zero')
        return cls(id=uuid4(), codigo_zoneamento='', codigo_propriedade=codigo_propriedade, zona=zona, aptidao_solo=aptidao_solo, area_zoneada_ha=round(area_zoneada_ha, 2), status=StatusZoneamento.ATIVO, data_zoneamento=date.today(), culturas_recomendadas=culturas_recomendadas or [], restricoes=restricoes or [], validade_ate=validade_ate, observacoes=observacoes)

    def entrar_revisao(self) -> None:
        if self.status == StatusZoneamento.REVOGADO:
            raise ValueError('Zoneamento revogado nao pode entrar em revisao')
        self.status = StatusZoneamento.EM_REVISAO

    def reativar(self, validade_ate: date | None=None) -> None:
        if self.status == StatusZoneamento.REVOGADO:
            raise ValueError('Zoneamento revogado nao pode ser reativado')
        self.status = StatusZoneamento.ATIVO
        self.validade_ate = validade_ate

    def revogar(self, motivo: str) -> None:
        if self.status == StatusZoneamento.REVOGADO:
            raise ValueError('Zoneamento ja esta revogado')
        self.status = StatusZoneamento.REVOGADO
        self.observacoes = motivo