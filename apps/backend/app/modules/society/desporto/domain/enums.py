from enum import StrEnum


class TipoAtleta(StrEnum):
    AMADOR = "amador"
    PROFISSIONAL = "profissional"
    SEMIPROFISSIONAL = "semiprofissional"
    DE_BASE = "de_base"
    MASTER = "master"
    PARALIMPICO = "paralimpico"


class ModalidadeDesportiva(StrEnum):
    FUTEBOL = "futebol"
    FUTSAL = "futsal"
    ANDEBOL = "andebol"
    BASQUETEBOL = "basquetebol"
    VOLEIBOL = "voleibol"
    ATLETISMO = "atletismo"
    NATACAO = "natacao"
    GINASTICA = "ginastica"
    JUDO = "judo"
    KARATE = "karate"
    BOXE = "boxe"
    TENIS = "tenis"
    CICLISMO = "ciclismo"
    DESPORTO_ADAPTADO = "desporto_adaptado"


class PosicaoAtleta(StrEnum):
    GUARDA_REDES = "guarda_redes"
    DEFESA = "defesa"
    MEDIO = "medio"
    AVANCADO = "avancado"
    BASE = "base"
    EXTREMO = "extremo"
    POSTE = "poste"
    PIVO = "pivo"
    CENTRAL = "central"
    LIBERO = "libero"


class PePreferencial(StrEnum):
    DIREITO = "direito"
    ESQUERDO = "esquerdo"
    AMBOS = "ambos"


class StatusAtleta(StrEnum):
    ATIVO = "ativo"
    LESIONADO = "lesionado"
    SUSPENSO = "suspenso"
    APOSENTADO = "aposentado"
    TRANSFERENCIA = "transferencia"
    EMPRESTIMO = "emprestimo"


class TipoCompeticao(StrEnum):
    CAMPEONATO = "campeonato"
    TORNEIO = "torneio"
    COPA = "copa"
    LIGA = "liga"
    PROVA = "prova"


class StatusCompeticao(StrEnum):
    PLANEADA = "planeada"
    INSCRICOES_ABERTAS = "inscricoes_abertas"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"


class TipoClube(StrEnum):
    PROFISSIONAL = "profissional"
    ESCOLAR = "escolar"
    UNIVERSITARIO = "universitario"
    COMUNITARIO = "comunitario"
    FEDERADO = "federado"


class StatusJogo(StrEnum):
    AGENDADO = "agendado"
    EM_ANDAMENTO = "em_andamento"
    ENCERRADO = "encerrado"
    CANCELADO = "cancelado"


class TipoEstadio(StrEnum):
    ESTADIO = "estadio"
    ARENA = "arena"
    PAVILHAO = "pavilhao"
    CAMPO = "campo"


class EstadoRelvado(StrEnum):
    NATURAL = "natural"
    SINTETICO = "sintetico"
    HIBRIDO = "hibrido"


class StatusTransferencia(StrEnum):
    EM_NEGOCIACAO = "em_negociacao"
    APROVADA = "aprovada"
    REJEITADA = "rejeitada"
    CANCELADA = "cancelada"
    CONCLUIDA = "concluida"


class TipoContrato(StrEnum):
    TEMPORADA = "temporada"
    MULTI_ANOS = "multi_anos"
    EMPRESTIMO = "emprestimo"
    FORMACAO = "formacao"


class StatusContrato(StrEnum):
    ATIVO = "ativo"
    SUSPENSO = "suspenso"
    ENCERRADO = "encerrado"
    RESCINDIDO = "rescindido"
