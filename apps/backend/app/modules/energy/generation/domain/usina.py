from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.energy.domain.enums import FonteEnergia, StatusUsina, TipoUsina

@dataclass
class Usina:
    id: UUID
    codigo_aneel: str
    nome: str
    fonte: FonteEnergia
    tipo: TipoUsina
    status: StatusUsina
    potencia_instalada_mw: Decimal
    proprietario_id: UUID
    proprietario_tipo: str
    municipio: str
    provincia: str
    potencia_fiscalizada_mw: Decimal | None = None
    garantia_fisica_mw: Decimal | None = None
    energia_assegurada_mwm: Decimal | None = None
    operador_id: UUID | None = None
    concessionaria_id: UUID | None = None
    outorga_id: UUID | None = None
    licenca_operacao_id: UUID | None = None
    data_autorizacao: date | None = None
    data_inicio_construcao: date | None = None
    data_entrada_operacao: date | None = None
    data_validade_outorga: date | None = None
    bacia_hidrografica: str | None = None
    rio: str | None = None
    area_reservatorio_km2: Decimal | None = None
    volume_reservatorio_hm3: Decimal | None = None
    area_ocupada_ha: Decimal | None = None
    numero_aerogeradores: int | None = None
    altura_torre_m: Decimal | None = None
    diametro_rotor_m: Decimal | None = None
    potencia_por_aerogerador_mw: Decimal | None = None
    numero_paineis: int | None = None
    area_paineis_m2: Decimal | None = None
    tecnologia: str | None = None
    combustivel: str | None = None
    consumo_combustivel: Decimal | None = None
    unidade_consumo: str | None = None
    rendimento: Decimal | None = None
    coordenadas_lat: Decimal | None = None
    coordenadas_long: Decimal | None = None
    observacoes: str | None = None

    @classmethod
    def cadastrar(cls, *, codigo_aneel: str, nome: str, fonte: FonteEnergia, tipo: TipoUsina, potencia_instalada_mw: Decimal, proprietario_id: UUID, proprietario_tipo: str, municipio: str, provincia: str) -> 'Usina':
        if not codigo_aneel.strip():
            raise ValueError('Codigo ANEEL e obrigatorio')
        if potencia_instalada_mw <= Decimal('0'):
            raise ValueError('Potencia instalada deve ser maior que zero')
        if not nome.strip():
            raise ValueError('Nome da usina e obrigatorio')
        return cls(id=uuid4(), codigo_aneel=codigo_aneel.strip().upper(), nome=nome.strip(), fonte=fonte, tipo=tipo, status=StatusUsina.PROJETO, potencia_instalada_mw=potencia_instalada_mw, proprietario_id=proprietario_id, proprietario_tipo=proprietario_tipo.strip(), municipio=municipio.strip(), provincia=provincia.strip())

    def iniciar_construcao(self, data_inicio: date) -> None:
        if self.status != StatusUsina.PROJETO:
            raise ValueError('Usina precisa estar em fase de projeto')
        self.status = StatusUsina.CONSTRUCAO
        self.data_inicio_construcao = data_inicio

    def iniciar_operacao(self, data_operacao: date) -> None:
        if self.status != StatusUsina.CONSTRUCAO:
            raise ValueError('Usina precisa estar em construcao')
        self.status = StatusUsina.OPERACAO
        self.data_entrada_operacao = data_operacao

    def paralisar(self, motivo: str) -> None:
        if self.status != StatusUsina.OPERACAO:
            raise ValueError('Apenas usinas em operacao podem ser paralisadas')
        if not motivo.strip():
            raise ValueError('Motivo da paralisacao e obrigatorio')
        self.status = StatusUsina.PARALISADA
        self.observacoes = motivo.strip()

    def desativar(self, motivo: str) -> None:
        if self.status == StatusUsina.DESATIVADA:
            raise ValueError('Usina ja esta desativada')
        if not motivo.strip():
            raise ValueError('Motivo da desativacao e obrigatorio')
        self.status = StatusUsina.DESATIVADA
        self.observacoes = motivo.strip()

    def vincular_outorga(self, outorga_id: UUID, data_validade: date) -> None:
        self.outorga_id = outorga_id
        self.data_validade_outorga = data_validade

    def atualizar_potencia_fiscalizada(self, potencia: Decimal) -> None:
        if potencia <= Decimal('0'):
            raise ValueError('Potencia fiscalizada deve ser maior que zero')
        self.potencia_fiscalizada_mw = potencia

    def atualizar_garantia_fisica(self, garantia: Decimal) -> None:
        if garantia <= Decimal('0'):
            raise ValueError('Garantia fisica deve ser maior que zero')
        self.garantia_fisica_mw = garantia