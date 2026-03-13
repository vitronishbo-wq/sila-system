from enum import Enum

class TipoOperadora(str, Enum):
    CONCESSIONARIA = 'concessionaria'
    PERMISSIONARIA = 'permissionaria'
    AUTORIZATARIA = 'autorizataria'
    PROVEDOR = 'provedor'
    SATELITAL = 'satelital'

class TipoServico(str, Enum):
    TELEFONIA_FIXA = 'telefonia_fixa'
    TELEFONIA_MOVEL = 'telefonia_movel'
    INTERNET_FIXA = 'internet_fixa'
    INTERNET_MOVEL = 'internet_movel'
    TV_ASSINATURA = 'tv_assinatura'
    RADIO = 'radio'
    COMUNICACAO_DADOS = 'comunicacao_dados'

class StatusOutorga(str, Enum):
    REQUERIDA = 'requerida'
    EM_ANALISE = 'em_analise'
    DEFERIDA = 'deferida'
    INDEFERIDA = 'indeferida'
    VENCIDA = 'vencida'
    RENOVADA = 'renovada'
    CANCELADA = 'cancelada'

class TipoPlano(str, Enum):
    PRE_PAGO = 'pre_pago'
    POS_PAGO = 'pos_pago'
    CONTROLE = 'controle'
    CORPORATIVO = 'corporativo'
    EMPRESARIAL = 'empresarial'
    GOVERNAMENTAL = 'governamental'

class StatusAssinante(str, Enum):
    ATIVO = 'ativo'
    SUSPENSO = 'suspenso'
    CANCELADO = 'cancelado'
    INADIMPLENTE = 'inadimplente'

class TipoInfraestrutura(str, Enum):
    TORRE = 'torre'
    ANTENA = 'antena'
    ERB = 'erb'
    DATACENTER = 'datacenter'
    BACKBONE = 'backbone'
    FIBRA_OPTICA = 'fibra_optica'
    CABO_SUBMARINO = 'cabo_submarino'
    POP = 'pop'
    ESTACAO_TERRENA = 'estacao_terrena'

class StatusInfraestrutura(str, Enum):
    PLANEADA = 'planeada'
    ATIVA = 'ativa'
    MANUTENCAO = 'manutencao'
    DESATIVADA = 'desativada'

class TipoOutorga(str, Enum):
    CONCESSAO = 'concessao'
    PERMISSAO = 'permissao'
    AUTORIZACAO = 'autorizacao'
    LICENCA = 'licenca'

class TipoEspectro(str, Enum):
    BANDA_LARGA = 'banda_larga'
    BANDA_ESTREITA = 'banda_estreita'
    RADIO_DIFUSAO = 'radio_difusao'
    TV_DIFUSAO = 'tv_difusao'
    SATELITE = 'satelite'

class StatusEspectro(str, Enum):
    DISPONIVEL = 'disponivel'
    OUTORGADO = 'outorgado'
    INTERFERIDO = 'interferido'
    RESERVA = 'reserva'

class StatusSLA(str, Enum):
    ATIVO = 'ativo'
    SUSPENSO = 'suspenso'
    ENCERRADO = 'encerrado'

class StatusQualidadeServico(str, Enum):
    CONFORME = 'conforme'
    ALERTA = 'alerta'
    CRITICO = 'critico'

class StatusIndicadorQualidade(str, Enum):
    BOM = 'bom'
    REGULAR = 'regular'
    CRITICO = 'critico'

class StatusFaturaTelecom(str, Enum):
    PENDENTE = 'pendente'
    PAGA = 'paga'
    VENCIDA = 'vencida'
    CANCELADA = 'cancelada'

class TipoReclamacaoTelecom(str, Enum):
    COBRANCA = 'cobranca'
    QUALIDADE = 'qualidade'
    COBERTURA = 'cobertura'
    ATENDIMENTO = 'atendimento'
    OUTROS = 'outros'

class StatusReclamacaoTelecom(str, Enum):
    ABERTA = 'aberta'
    EM_TRATAMENTO = 'em_tratamento'
    FECHADA = 'fechada'