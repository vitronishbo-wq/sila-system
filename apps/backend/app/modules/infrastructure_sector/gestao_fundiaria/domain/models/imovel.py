from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import NaturezaImovel, RegimePropriedade, SituacaoDominial, TipoImovel

@dataclass
class Imovel:
    id: UUID
    inscricao_imobiliaria: str
    tipo: TipoImovel
    natureza: NaturezaImovel
    regime: RegimePropriedade
    situacao: SituacaoDominial
    area_total: Decimal
    endereco: str
    bairro: str
    municipio: str
    provincia: str
    data_cadastro: date
    area_privativa: Decimal | None = None
    area_construida: Decimal | None = None
    area_terreno: Decimal | None = None
    cep: str | None = None
    coordenadas_lat: Decimal | None = None
    coordenadas_long: Decimal | None = None
    matricula_id: UUID | None = None
    proprietario_atual_id: UUID | None = None
    data_atualizacao: date | None = None
    ativo: bool = True
    observacoes: str | None = None

    @classmethod
    def cadastrar(cls, *, tipo: TipoImovel, natureza: NaturezaImovel, area_total: Decimal, endereco: str, bairro: str, municipio: str, provincia: str, inscricao_imobiliaria: str) -> 'Imovel':
        if not inscricao_imobiliaria.strip():
            raise ValueError('Inscricao imobiliaria e obrigatoria')
        if area_total <= Decimal('0'):
            raise ValueError('Area total deve ser maior que zero')
        if not endereco.strip():
            raise ValueError('Endereco e obrigatorio')
        if not bairro.strip():
            raise ValueError('Bairro e obrigatorio')
        if not municipio.strip():
            raise ValueError('Municipio e obrigatorio')
        if not provincia.strip():
            raise ValueError('Provincia e obrigatoria')
        return cls(id=uuid4(), inscricao_imobiliaria=inscricao_imobiliaria.strip(), tipo=tipo, natureza=natureza, regime=RegimePropriedade.PLENA, situacao=SituacaoDominial.REGULAR, area_total=area_total.quantize(Decimal('0.01')), endereco=endereco.strip(), bairro=bairro.strip(), municipio=municipio.strip(), provincia=provincia.strip(), data_cadastro=date.today(), ativo=True)

    def atualizar_area(self, area_total: Decimal) -> None:
        if area_total <= Decimal('0'):
            raise ValueError('Area total deve ser maior que zero')
        self.area_total = area_total.quantize(Decimal('0.01'))
        self.data_atualizacao = date.today()

    def atualizar_proprietario(self, proprietario_id: UUID) -> None:
        self.proprietario_atual_id = proprietario_id
        self.data_atualizacao = date.today()

    def atualizar_situacao(self, situacao: SituacaoDominial) -> None:
        self.situacao = situacao
        self.data_atualizacao = date.today()

    def desativar(self, motivo: str) -> None:
        if not motivo.strip():
            raise ValueError('Motivo da desativacao e obrigatorio')
        self.ativo = False
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()

    def vincular_matricula(self, matricula_id: UUID) -> None:
        self.matricula_id = matricula_id
        self.data_atualizacao = date.today()