from enum import Enum

class TipoAtleta(str, Enum):
    AMADOR = 'amador'
    PROFISSIONAL = 'profissional'
    SEMIPROFISSIONAL = 'semiprofissional'
    DE_BASE = 'de_base'
    MASTER = 'master'
    PARALIMPICO = 'paralimpico'

class ModalidadeDesportiva(str, Enum):
    FUTEBOL = 'futebol'
    FUTSAL = 'futsal'
    ANDEBOL = 'andebol'
    BASQUETEBOL = 'basquetebol'
    VOLEIBOL = 'voleibol'
    ATLETISMO = 'atletismo'
    NATACAO = 'natacao'
    GINASTICA = 'ginastica'
    JUDO = 'judo'
    KARATE = 'karate'
    BOXE = 'boxe'
    TENIS = 'tenis'
    CICLISMO = 'ciclismo'
    DESPORTO_ADAPTADO = 'desporto_adaptado'

class PosicaoAtleta(str, Enum):
    GUARDA_REDES = 'guarda_redes'
    DEFESA = 'defesa'
    MEDIO = 'medio'
    AVANCADO = 'avancado'
    BASE = 'base'
    EXTREMO = 'extremo'
    POSTE = 'poste'
    PIVO = 'pivo'
    CENTRAL = 'central'
    LIBERO = 'libero'

class PePreferencial(str, Enum):
    DIREITO = 'direito'
    ESQUERDO = 'esquerdo'
    AMBOS = 'ambos'

class StatusAtleta(str, Enum):
    ATIVO = 'ativo'
    LESIONADO = 'lesionado'
    SUSPENSO = 'suspenso'
    APOSENTADO = 'aposentado'
    TRANSFERENCIA = 'transferencia'
    EMPRESTIMO = 'emprestimo'

class TipoCompeticao(str, Enum):
    CAMPEONATO = 'campeonato'
    TORNEIO = 'torneio'
    COPA = 'copa'
    LIGA = 'liga'
    PROVA = 'prova'

class StatusCompeticao(str, Enum):
    PLANEADA = 'planeada'
    INSCRICOES_ABERTAS = 'inscricoes_abertas'
    EM_ANDAMENTO = 'em_andamento'
    CONCLUIDA = 'concluida'
    CANCELADA = 'cancelada'

class TipoClube(str, Enum):
    PROFISSIONAL = 'profissional'
    ESCOLAR = 'escolar'
    UNIVERSITARIO = 'universitario'
    COMUNITARIO = 'comunitario'
    FEDERADO = 'federado'

class StatusJogo(str, Enum):
    AGENDADO = 'agendado'
    EM_ANDAMENTO = 'em_andamento'
    ENCERRADO = 'encerrado'
    CANCELADO = 'cancelado'

class TipoEstadio(str, Enum):
    ESTADIO = 'estadio'
    ARENA = 'arena'
    PAVILHAO = 'pavilhao'
    CAMPO = 'campo'

class EstadoRelvado(str, Enum):
    NATURAL = 'natural'
    SINTETICO = 'sintetico'
    HIBRIDO = 'hibrido'

class StatusTransferencia(str, Enum):
    EM_NEGOCIACAO = 'em_negociacao'
    APROVADA = 'aprovada'
    REJEITADA = 'rejeitada'
    CANCELADA = 'cancelada'
    CONCLUIDA = 'concluida'

class TipoContrato(str, Enum):
    TEMPORADA = 'temporada'
    MULTI_ANOS = 'multi_anos'
    EMPRESTIMO = 'emprestimo'
    FORMACAO = 'formacao'

class StatusContrato(str, Enum):
    ATIVO = 'ativo'
    SUSPENSO = 'suspenso'
    ENCERRADO = 'encerrado'
    RESCINDIDO = 'rescindido'