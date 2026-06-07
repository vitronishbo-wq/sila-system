from enum import StrEnum


class TipoOperadora(StrEnum):
    CONCESSIONARIA = "concessionaria"
    PERMISSIONARIA = "permissionaria"
    AUTORIZATARIA = "autorizataria"
    PROVEDOR = "provedor"
    SATELITAL = "satelital"


class TipoServico(StrEnum):
    TELEFONIA_FIXA = "telefonia_fixa"
    TELEFONIA_MOVEL = "telefonia_movel"
    INTERNET_FIXA = "internet_fixa"
    INTERNET_MOVEL = "internet_movel"
    TV_ASSINATURA = "tv_assinatura"
    RADIO = "radio"
    COMUNICACAO_DADOS = "comunicacao_dados"


class StatusOutorga(StrEnum):
    REQUERIDA = "requerida"
    EM_ANALISE = "em_analise"
    DEFERIDA = "deferida"
    INDEFERIDA = "indeferida"
    VENCIDA = "vencida"
    RENOVADA = "renovada"
    CANCELADA = "cancelada"


class TipoPlano(StrEnum):
    PRE_PAGO = "pre_pago"
    POS_PAGO = "pos_pago"
    CONTROLE = "controle"
    CORPORATIVO = "corporativo"
    EMPRESARIAL = "empresarial"
    GOVERNAMENTAL = "governamental"


class StatusAssinante(StrEnum):
    ATIVO = "ativo"
    SUSPENSO = "suspenso"
    CANCELADO = "cancelado"
    INADIMPLENTE = "inadimplente"


class TipoInfraestrutura(StrEnum):
    TORRE = "torre"
    ANTENA = "antena"
    ERB = "erb"
    DATACENTER = "datacenter"
    BACKBONE = "backbone"
    FIBRA_OPTICA = "fibra_optica"
    CABO_SUBMARINO = "cabo_submarino"
    POP = "pop"
    ESTACAO_TERRENA = "estacao_terrena"


class StatusInfraestrutura(StrEnum):
    PLANEADA = "planeada"
    ATIVA = "ativa"
    MANUTENCAO = "manutencao"
    DESATIVADA = "desativada"


class TipoOutorga(StrEnum):
    CONCESSAO = "concessao"
    PERMISSAO = "permissao"
    AUTORIZACAO = "autorizacao"
    LICENCA = "licenca"


class TipoEspectro(StrEnum):
    BANDA_LARGA = "banda_larga"
    BANDA_ESTREITA = "banda_estreita"
    RADIO_DIFUSAO = "radio_difusao"
    TV_DIFUSAO = "tv_difusao"
    SATELITE = "satelite"


class StatusEspectro(StrEnum):
    DISPONIVEL = "disponivel"
    OUTORGADO = "outorgado"
    INTERFERIDO = "interferido"
    RESERVA = "reserva"


class StatusSLA(StrEnum):
    ATIVO = "ativo"
    SUSPENSO = "suspenso"
    ENCERRADO = "encerrado"


class StatusQualidadeServico(StrEnum):
    CONFORME = "conforme"
    ALERTA = "alerta"
    CRITICO = "critico"


class StatusIndicadorQualidade(StrEnum):
    BOM = "bom"
    REGULAR = "regular"
    CRITICO = "critico"


class StatusFaturaTelecom(StrEnum):
    PENDENTE = "pendente"
    PAGA = "paga"
    VENCIDA = "vencida"
    CANCELADA = "cancelada"


class TipoReclamacaoTelecom(StrEnum):
    COBRANCA = "cobranca"
    QUALIDADE = "qualidade"
    COBERTURA = "cobertura"
    ATENDIMENTO = "atendimento"
    OUTROS = "outros"


class StatusReclamacaoTelecom(StrEnum):
    ABERTA = "aberta"
    EM_TRATAMENTO = "em_tratamento"
    FECHADA = "fechada"
