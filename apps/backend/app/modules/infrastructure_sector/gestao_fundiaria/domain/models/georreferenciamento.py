from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

@dataclass
class Georreferenciamento:
    id: UUID
    codigo_geo: str
    imovel_inscricao: str
    latitude: Decimal
    longitude: Decimal
    sistema_referencia: str
    data_registro: date
    precisao_metros: Decimal | None = None
    area_calculada: Decimal | None = None
    validado: bool = True
    ativo: bool = True
    data_atualizacao: date | None = None
    observacoes: str | None = None

    @classmethod
    def registrar(cls, *, codigo_geo: str, imovel_inscricao: str, latitude: Decimal, longitude: Decimal, sistema_referencia: str='WGS84', precisao_metros: Decimal | None=None, area_calculada: Decimal | None=None) -> 'Georreferenciamento':
        if not codigo_geo.strip():
            raise ValueError('Codigo georreferenciado e obrigatorio')
        if not imovel_inscricao.strip():
            raise ValueError('Inscricao do imovel e obrigatoria')
        if latitude < Decimal('-90') or latitude > Decimal('90'):
            raise ValueError('Latitude fora do intervalo valido')
        if longitude < Decimal('-180') or longitude > Decimal('180'):
            raise ValueError('Longitude fora do intervalo valido')
        if not sistema_referencia.strip():
            raise ValueError('Sistema de referencia e obrigatorio')
        if precisao_metros is not None and precisao_metros < Decimal('0'):
            raise ValueError('Precisao em metros deve ser positiva')
        if area_calculada is not None and area_calculada <= Decimal('0'):
            raise ValueError('Area calculada deve ser maior que zero')
        return cls(id=uuid4(), codigo_geo=codigo_geo.strip(), imovel_inscricao=imovel_inscricao.strip(), latitude=latitude.quantize(Decimal('0.00000001')), longitude=longitude.quantize(Decimal('0.00000001')), sistema_referencia=sistema_referencia.strip().upper(), data_registro=date.today(), precisao_metros=precisao_metros.quantize(Decimal('0.01')) if precisao_metros is not None else None, area_calculada=area_calculada.quantize(Decimal('0.01')) if area_calculada is not None else None, validado=True, ativo=True)

    def atualizar_ponto(self, *, latitude: Decimal, longitude: Decimal) -> None:
        if latitude < Decimal('-90') or latitude > Decimal('90'):
            raise ValueError('Latitude fora do intervalo valido')
        if longitude < Decimal('-180') or longitude > Decimal('180'):
            raise ValueError('Longitude fora do intervalo valido')
        self.latitude = latitude.quantize(Decimal('0.00000001'))
        self.longitude = longitude.quantize(Decimal('0.00000001'))
        self.data_atualizacao = date.today()

    def invalidar(self, motivo: str) -> None:
        if not motivo.strip():
            raise ValueError('Motivo da invalidacao e obrigatorio')
        self.validado = False
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()