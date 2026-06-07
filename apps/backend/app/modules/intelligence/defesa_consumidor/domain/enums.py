from enum import StrEnum


class StatusReclamacao(StrEnum):
    ABERTA = "aberta"
    EM_ANALISE = "em_analise"
    EM_MEDIACAO = "em_mediacao"
    AGUARDANDO_CONSUMIDOR = "aguardando_consumidor"
    AGUARDANDO_ESTABELECIMENTO = "aguardando_estabelecimento"
    ENCERRADA = "encerrada"
    CANCELADA = "cancelada"


class Prioridade(StrEnum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


class CategoriaReclamacao(StrEnum):
    PRODUTO_DEFECTUOSO = "produto_defectuoso"
    SERVICO_NAO_PRESTADO = "servico_nao_prestado"
    PROPAGANDA_ENGANOSA = "propaganda_enganosa"
    COBRANCA_INDEVIDA = "cobranca_indevida"
    ATENDIMENTO_INADEQUADO = "atendimento_inadequado"
    RECUSA_VENDA = "recusa_venda"
    OUTROS = "outros"


class TipoSancao(StrEnum):
    ADVERTENCIA = "advertencia"
    MULTA = "multa"
    SUSPENSAO = "suspensao"
    CASSACAO = "cassacao"
    INTERDICACAO = "interdicacao"


class StatusMediacao(StrEnum):
    AGENDADA = "agendada"
    EM_ANDAMENTO = "em_andamento"
    SUSPENSA = "suspensa"
    CONCLUIDA = "concluida"
    FRUSTRADA = "frustrada"
