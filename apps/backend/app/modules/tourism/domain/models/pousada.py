from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from app.modules.tourism.domain.enums import ClassificacaoHoteleira, TipoMeioHospedagem

@dataclass
class Pousada:
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
    proprietario_id: UUID
    data_abertura: date
    ativa: bool = True
    site: str | None = None
    observacoes: str | None = None

    @classmethod
    def cadastrar(cls, *, nome: str, classificacao: ClassificacaoHoteleira, cnpj: str, endereco: str, numero: str, bairro: str, municipio: str, provincia: str, cep: str, telefone: str, email: str, quartos: int, capacidade_maxima: int, proprietario_id: UUID) -> 'Pousada':
        if quartos <= 0:
            raise ValueError('Quantidade de quartos deve ser maior que zero')
        if capacidade_maxima <= 0:
            raise ValueError('Capacidade maxima deve ser maior que zero')
        return cls(id=uuid4(), cadastur='', nome=nome.strip(), tipo=TipoMeioHospedagem.POUSADA, classificacao=classificacao, cnpj=cnpj.strip(), endereco=endereco.strip(), numero=numero.strip(), bairro=bairro.strip(), municipio=municipio.strip(), provincia=provincia.strip(), cep=cep.strip(), telefone=telefone.strip(), email=email.strip().lower(), quartos=quartos, capacidade_maxima=capacidade_maxima, proprietario_id=proprietario_id, data_abertura=date.today(), ativa=True)

    def atualizar_dados(self, *, nome: str | None=None, endereco: str | None=None, numero: str | None=None, bairro: str | None=None, municipio: str | None=None, provincia: str | None=None, cep: str | None=None, telefone: str | None=None, email: str | None=None, site: str | None=None, observacoes: str | None=None, classificacao: ClassificacaoHoteleira | None=None) -> None:
        if nome is not None:
            self.nome = nome.strip()
        if endereco is not None:
            self.endereco = endereco.strip()
        if numero is not None:
            self.numero = numero.strip()
        if bairro is not None:
            self.bairro = bairro.strip()
        if municipio is not None:
            self.municipio = municipio.strip()
        if provincia is not None:
            self.provincia = provincia.strip()
        if cep is not None:
            self.cep = cep.strip()
        if telefone is not None:
            self.telefone = telefone.strip()
        if email is not None:
            self.email = email.strip().lower()
        if site is not None:
            self.site = site.strip() if site else None
        if observacoes is not None:
            self.observacoes = observacoes.strip() if observacoes else None
        if classificacao is not None:
            self.classificacao = classificacao

    def desativar(self) -> None:
        self.ativa = False

    def ativar(self) -> None:
        self.ativa = True
