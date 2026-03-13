from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.resources.ambiente.domain.enums import Bioma, TipoImovel

@dataclass
class ImovelRural:
    id: UUID
    codigo_imovel: str
    proprietario_id: UUID
    nome: str
    provincia: str
    municipio: str
    area_total: Decimal
    bioma: Bioma
    tipo_imovel: TipoImovel
    coordenadas: str | None
    data_cadastro: date
    ativo: bool = True

    @classmethod
    def criar(cls, *, proprietario_id: UUID, nome: str, provincia: str, municipio: str, area_total: Decimal, bioma: Bioma, tipo_imovel: TipoImovel, coordenadas: str | None=None) -> 'ImovelRural':
        if area_total <= Decimal('0'):
            raise ValueError('Area total deve ser maior que zero')
        return cls(id=uuid4(), codigo_imovel='', proprietario_id=proprietario_id, nome=nome.strip(), provincia=provincia.strip(), municipio=municipio.strip(), area_total=area_total.quantize(Decimal('0.01')), bioma=bioma, tipo_imovel=tipo_imovel, coordenadas=coordenadas, data_cadastro=date.today(), ativo=True)