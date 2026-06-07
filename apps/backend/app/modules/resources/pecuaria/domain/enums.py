from enum import Enum


class TipoAnimal(Enum):
    BOVINO = "bovino"
    CAPRINO = "caprino"
    OVINO = "ovino"
    SUINO = "suino"
    EQUINO = "equino"
    BUFALINO = "bufalino"
    AVES = "aves"


class Sexo(Enum):
    MACHO = "macho"
    FEMEA = "femea"


class StatusAnimal(Enum):
    ATIVO = "ativo"
    VENDIDO = "vendido"
    MORTO = "morto"
    ABATIDO = "abatido"
    DESCARTADO = "descartado"


class TipoProducao(Enum):
    LEITE = "leite"
    CARNE = "carne"
    OVOS = "ovos"
    LA = "la"
    COURO = "couro"
    REPRODUCAO = "reproducao"


class StatusPecuarista(Enum):
    PENDENTE = "pendente"
    ATIVO = "ativo"
    SUSPENSO = "suspenso"
    INATIVO = "inativo"


class StatusRebanho(Enum):
    ATIVO = "ativo"
    ENCERRADO = "encerrado"


class TipoInstalacao(Enum):
    CURRAL = "curral"
    ESTABULO = "estabulo"
    APRISCO = "aprisco"
    CHIQUEIRO = "chiqueiro"
    COCHEIRA = "cocheira"
