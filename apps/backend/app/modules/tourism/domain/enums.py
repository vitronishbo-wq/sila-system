from enum import StrEnum


class TipoOperadorTuristico(StrEnum):
    AGENCIA_VIAGENS = "agencia_viagens"
    OPERADORA = "operadora"
    MEIO_HOSPEDAGEM = "meio_hospedagem"
    TRANSPORTADORA = "transportadora"
    RESTAURANTE = "restaurante"
    GUIA_TURISMO = "guia_turismo"
    CONDUTOR = "condutor"


class TipoMeioHospedagem(StrEnum):
    HOTEL = "hotel"
    POUSADA = "pousada"
    RESORT = "resort"
    LODGE = "lodge"
    CAMPING = "camping"
    HOSTEL = "hostel"
    ALBERGUE = "albergue"


class ClassificacaoHoteleira(StrEnum):
    SIMPLES = "simples"
    ECONOMICO = "economico"
    CONFORT = "confort"
    SUPERIOR = "superior"
    LUXO = "luxo"
    SUPER_LUXO = "super_luxo"


class TipoAtracao(StrEnum):
    NATURAL = "natural"
    CULTURAL = "cultural"
    HISTORICA = "historica"
    ARQUEOLOGICA = "arqueologica"
    RELIGIOSA = "religiosa"
    AVENTURA = "aventura"
    GASTRONOMICA = "gastronomica"
    EVENTO = "evento"


class StatusReserva(StrEnum):
    PENDENTE = "pendente"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    REALIZADA = "realizada"
    NO_SHOW = "no_show"


class TipoTarifa(StrEnum):
    NORMAL = "normal"
    PROMOCIONAL = "promocional"
    GRUPO = "grupo"
    CORPORATIVA = "corporativa"
    CONVENIO = "convenio"


class Temporada(StrEnum):
    ALTA = "alta"
    MEDIA = "media"
    BAIXA = "baixa"
    FERIADO = "feriado"
    EVENTO = "evento"
