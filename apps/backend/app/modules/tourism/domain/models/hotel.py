from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4
from app.modules.tourism.domain.enums import ClassificacaoHoteleira, TipoMeioHospedagem

@dataclass
class Hotel:
    id: UUID
    cadastur: str
    nome: str
    tipo: TipoMeioHospedagem
    classificacao: ClassificacaoHoteleira
    cnpj: str
    endereco: str
    numero: str
    bairro: str
    municipio: str
    provincia: str
    cep: str
    telefone: str
    email: str
    quartos: int
    capacidade_maxima: int
    categoria_estrelas: int
    proprietario_id: UUID
    data_abertura: date
    inscricao_estadual: Optional[str] = None
    inscricao_municipal: Optional[str] = None
    complemento: Optional[str] = None
    coordenadas_lat: Optional[Decimal] = None
    coordenadas_long: Optional[Decimal] = None
    site: Optional[str] = None
    area_comum: Optional[list[str]] = None
    servicos: Optional[list[str]] = None
    acessibilidade: bool = False
    pet_friendly: bool = False
    wifi: bool = True
    estacionamento: bool = False
    piscina: bool = False
    academia: bool = False
    restaurante: bool = False
    bar: bool = False
    sala_reunioes: bool = False
    centro_convencoes: bool = False
    responsavel_id: Optional[UUID] = None
    licenca_funcionamento: Optional[str] = None
    data_renovacao: Optional[date] = None
    observacoes: Optional[str] = None

    @classmethod
    def cadastrar(cls, *, nome: str, tipo: TipoMeioHospedagem, classificacao: ClassificacaoHoteleira, cnpj: str, endereco: str, numero: str, bairro: str, municipio: str, provincia: str, cep: str, telefone: str, email: str, quartos: int, capacidade_maxima: int, proprietario_id: UUID) -> 'Hotel':
        if quartos <= 0:
            raise ValueError('Quantidade de quartos deve ser maior que zero')
        if capacidade_maxima <= 0:
            raise ValueError('Capacidade maxima deve ser maior que zero')
        return cls(id=uuid4(), cadastur='', nome=nome.strip(), tipo=tipo, classificacao=classificacao, cnpj=cnpj.strip(), endereco=endereco.strip(), numero=numero.strip(), bairro=bairro.strip(), municipio=municipio.strip(), provincia=provincia.strip(), cep=cep.strip(), telefone=telefone.strip(), email=email.strip().lower(), quartos=quartos, capacidade_maxima=capacidade_maxima, categoria_estrelas=0, proprietario_id=proprietario_id, data_abertura=date.today())

    def atualizar_classificacao(self, estrelas: int) -> None:
        if estrelas < 1 or estrelas > 5:
            raise ValueError('Categoria de estrelas deve estar entre 1 e 5')
        self.categoria_estrelas = estrelas

    def adicionar_servico(self, servico: str) -> None:
        nome_servico = servico.strip()
        if not nome_servico:
            raise ValueError('Servico nao pode ser vazio')
        if self.servicos is None:
            self.servicos = []
        if nome_servico not in self.servicos:
            self.servicos.append(nome_servico)
