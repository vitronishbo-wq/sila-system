from enum import Enum


class TipoOperadorTuristico(str, Enum):
    AGENCIA_VIAGENS = "agencia_viagens"
    OPERADORA = "operadora"
    MEIO_HOSPEDAGEM = "meio_hospedagem"
    TRANSPORTADORA = "transportadora"
    RESTAURANTE = "restaurante"
    GUIA_TURISMO = "guia_turismo"
    CONDUTOR = "condutor"


class TipoMeioHospedagem(str, Enum):
    HOTEL = "hotel"
    POUSADA = "pousada"
    RESORT = "resort"
    LODGE = "lodge"
    CAMPING = "camping"
    HOSTEL = "hostel"
    ALBERGUE = "albergue"


class ClassificacaoHoteleira(str, Enum):
    SIMPLES = "simples"
    ECONOMICO = "economico"
    CONFORT = "confort"
    SUPERIOR = "superior"
    LUXO = "luxo"
    SUPER_LUXO = "super_luxo"


class TipoAtracao(str, Enum):
    NATURAL = "natural"
    CULTURAL = "cultural"
    HISTORICA = "historica"
    ARQUEOLOGICA = "arqueologica"
    RELIGIOSA = "religiosa"
    AVENTURA = "aventura"
    GASTRONOMICA = "gastronomica"
    EVENTO = "evento"


class StatusReserva(str, Enum):
    PENDENTE = "pendente"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    REALIZADA = "realizada"
    NO_SHOW = "no_show"


class TipoTarifa(str, Enum):
    NORMAL = "normal"
    PROMOCIONAL = "promocional"
    GRUPO = "grupo"
    CORPORATIVA = "corporativa"
    CONVENIO = "convenio"


class Temporada(str, Enum):
    ALTA = "alta"
    MEDIA = "media"
    BAIXA = "baixa"
    FERIADO = "feriado"
    EVENTO = "evento"
