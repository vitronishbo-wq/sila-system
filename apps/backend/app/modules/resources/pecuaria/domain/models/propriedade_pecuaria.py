from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

@dataclass
class PropriedadePecuaria:
    id: UUID
    codigo_propriedade: str
    pecuarista_id: UUID
    nome: str
    area_total_ha: float
    municipio: str
    provincia: str
    data_cadastro: date
    ativo: bool = True

    @classmethod
    def criar(cls, *, pecuarista_id: UUID, nome: str, area_total_ha: float, municipio: str, provincia: str) -> 'PropriedadePecuaria':
        if area_total_ha <= 0:
            raise ValueError('Area total deve ser maior que zero')
        return cls(id=uuid4(), codigo_propriedade='', pecuarista_id=pecuarista_id, nome=nome, area_total_ha=round(area_total_ha, 2), municipio=municipio, provincia=provincia, data_cadastro=date.today(), ativo=True)