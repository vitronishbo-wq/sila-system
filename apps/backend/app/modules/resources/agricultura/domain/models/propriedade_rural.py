from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.resources.agricultura.domain.enums import TipoPropriedade


@dataclass
class PropriedadeRural:
    id: UUID
    codigo_propriedade: str
    produtor_id: UUID
    nome: str
    tipo: TipoPropriedade
    area_total_ha: float
    area_cultivavel_ha: float
    provincia: str | None
    municipio: str | None
    data_cadastro: date
    ativo: bool = True

    @classmethod
    def criar(
        cls,
        *,
        produtor_id: UUID,
        nome: str,
        tipo: TipoPropriedade,
        area_total_ha: float,
        area_cultivavel_ha: float,
        provincia: str | None = None,
        municipio: str | None = None,
    ) -> PropriedadeRural:
        if area_total_ha <= 0:
            raise ValueError("Area total deve ser maior que zero")
        if area_cultivavel_ha < 0:
            raise ValueError("Area cultivavel nao pode ser negativa")
        if area_cultivavel_ha > area_total_ha:
            raise ValueError("Area cultivavel nao pode ser maior que area total")
        return cls(
            id=uuid4(),
            codigo_propriedade="",
            produtor_id=produtor_id,
            nome=nome,
            tipo=tipo,
            area_total_ha=round(area_total_ha, 2),
            area_cultivavel_ha=round(area_cultivavel_ha, 2),
            provincia=provincia,
            municipio=municipio,
            data_cadastro=date.today(),
            ativo=True,
        )
