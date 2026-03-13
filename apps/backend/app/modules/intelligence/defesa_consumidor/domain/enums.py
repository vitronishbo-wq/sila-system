from enum import Enum

class StatusReclamacao(str, Enum):
    ABERTA = 'aberta'
    EM_ANALISE = 'em_analise'
    EM_MEDIACAO = 'em_mediacao'
    AGUARDANDO_CONSUMIDOR = 'aguardando_consumidor'
    AGUARDANDO_ESTABELECIMENTO = 'aguardando_estabelecimento'
    ENCERRADA = 'encerrada'
    CANCELADA = 'cancelada'

class Prioridade(str, Enum):
    BAIXA = 'baixa'
    MEDIA = 'media'
    ALTA = 'alta'
    CRITICA = 'critica'

class CategoriaReclamacao(str, Enum):
    PRODUTO_DEFECTUOSO = 'produto_defectuoso'
    SERVICO_NAO_PRESTADO = 'servico_nao_prestado'
    PROPAGANDA_ENGANOSA = 'propaganda_enganosa'
    COBRANCA_INDEVIDA = 'cobranca_indevida'
    ATENDIMENTO_INADEQUADO = 'atendimento_inadequado'
    RECUSA_VENDA = 'recusa_venda'
    OUTROS = 'outros'

class TipoSancao(str, Enum):
    ADVERTENCIA = 'advertencia'
    MULTA = 'multa'
    SUSPENSAO = 'suspensao'
    CASSACAO = 'cassacao'
    INTERDICACAO = 'interdicacao'

class StatusMediacao(str, Enum):
    AGENDADA = 'agendada'
    EM_ANDAMENTO = 'em_andamento'
    SUSPENSA = 'suspensa'
    CONCLUIDA = 'concluida'
    FRUSTRADA = 'frustrada'