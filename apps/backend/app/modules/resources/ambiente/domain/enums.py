from enum import Enum


class TipoImovel(Enum):
    PEQUENA_PROPRIEDADE = "pequena_propriedade"
    MEDIA_PROPRIEDADE = "media_propriedade"
    GRANDE_PROPRIEDADE = "grande_propriedade"
    ASSENTAMENTO = "assentamento"
    TERRITORIO_QUILOMBOLA = "territorio_quilombola"
    TERRITORIO_INDIGENA = "territorio_indigena"


class Bioma(Enum):
    FLORESTA_TROPICAL = "floresta_tropical"
    SAVANA = "savana"
    MANGUEZAL = "manguezal"
    CERRADO = "cerrado"
    CAATINGA = "caatinga"
    PANTANAL = "pantanal"
    MATA_ATLANTICA = "mata_atlantica"
    PAMPA = "pampa"


class StatusCAR(Enum):
    PENDENTE = "pendente"
    EM_ANALISE = "em_analise"
    CADASTRADO = "cadastrado"
    PENDENCIA = "pendencia"
    SUSPENSO = "suspenso"
    CANCELADO = "cancelado"


class TipoLicenca(Enum):
    PREVIA = "previa"
    INSTALACAO = "instalacao"
    OPERACAO = "operacao"
    UNICA = "unica"
    SIMPLIFICADA = "simplificada"
    TRES_VIAS = "tres_vias"


class StatusLicenca(Enum):
    REQUERIDA = "requerida"
    EM_ANALISE = "em_analise"
    DEFERIDA = "deferida"
    INDEFERIDA = "indeferida"
    SUSPENSA = "suspensa"
    CANCELADA = "cancelada"
    VENCIDA = "vencida"


class TipoAutoInfracao(Enum):
    ADVERTENCIA = "advertencia"
    MULTA = "multa"
    EMBARGO = "embargo"
    APREENSAO = "apreensao"
    SUSPENSAO = "suspensao"


class StatusTACA(Enum):
    PROPOSTO = "proposto"
    EM_EXECUCAO = "em_execucao"
    CUMPRIDO = "cumprido"
    DESCUMPRIDO = "descumprido"
    REVOGADO = "revogado"


class TipoEstudoAmbiental(Enum):
    EIA = "eia"
    RIMA = "rima"
    PCA = "pca"
    RCA = "rca"


class StatusEstudoAmbiental(Enum):
    SUBMETIDO = "submetido"
    EM_ANALISE = "em_analise"
    APROVADO = "aprovado"
    COMPLEMENTACAO = "complementacao"
    REPROVADO = "reprovado"


class StatusCondicionante(Enum):
    PENDENTE = "pendente"
    EM_CUMPRIMENTO = "em_cumprimento"
    CUMPRIDA = "cumprida"
    VENCIDA = "vencida"
    DESCUMPRIDA = "descumprida"


class StatusFiscalizacao(Enum):
    AGENDADA = "agendada"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"


class StatusAutoInfracao(Enum):
    LAVRADO = "lavrado"
    NOTIFICADO = "notificado"
    EM_RECURSO = "em_recurso"
    JULGADO = "julgado"
    CANCELADO = "cancelado"


class StatusEmbargo(Enum):
    ATIVO = "ativo"
    SUSPENSO = "suspenso"
    LEVANTADO = "levantado"


class StatusMulta(Enum):
    APLICADA = "aplicada"
    PARCELADA = "parcelada"
    PAGA = "paga"
    VENCIDA = "vencida"
    CANCELADA = "cancelada"
